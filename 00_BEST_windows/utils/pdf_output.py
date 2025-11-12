import pandas as pd
import json
import os
import datetime
from PyQt6.QtGui import QTextDocument, QPageLayout
from PyQt6.QtCore import QMarginsF
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QApplication

SAVE_FILE = "recent_session.json"
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

import reportlab
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image
import json
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.graph_objects as go
import plotly.io as pio

from utils.save_progress import get_user_data_dir

import os, sys, subprocess

from pathlib import Path
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

def open_pdf(filepath):
    if sys.platform.startswith("darwin"):  # macOS
        subprocess.run(["open", filepath])
    elif os.name == "nt":  # Windows
        os.startfile(filepath)


def get_auto_text(df: pd.DataFrame):

    data_dir = get_user_data_dir()
    json_folder = data_dir / "Saved Progress"

    excel_file_path_1 = json_folder / "key_values_in_excel.xlsx"
    key_values_in_excel = pd.read_excel(excel_file_path_1, sheet_name=None)

    final_energy_before = key_values_in_excel["values"].iloc[2, 1]
    final_energy_after = key_values_in_excel["values"].iloc[2, 2]
    final_energy_ibp = key_values_in_excel["values"].iloc[2, 3]
    final_energy_reduction = final_energy_before - final_energy_after
    final_energy_difference_ibp = final_energy_ibp - final_energy_after

    cement_intensity_before = key_values_in_excel["values"].iloc[3, 1]
    cement_intensity_after = key_values_in_excel["values"].iloc[3, 2]
    cement_intensity_ibp = key_values_in_excel["values"].iloc[3, 3]
    cement_intensity_reduction = cement_intensity_before - cement_intensity_after
    cement_intensity_difference_ibp = cement_intensity_ibp - cement_intensity_after

    total_emissions_before = key_values_in_excel["values"].iloc[6, 1]
    total_emissions_after = key_values_in_excel["values"].iloc[6, 2]
    total_emissions_ibp = key_values_in_excel["values"].iloc[6, 3]
    total_emissions_reduction = total_emissions_before - total_emissions_after
    total_emissions_difference_ibp = total_emissions_ibp - total_emissions_after

    cement_emissions_intensity_before = key_values_in_excel["values"].iloc[7, 1]
    cement_emissions_intensity_after = key_values_in_excel["values"].iloc[7, 2]
    cement_emissions_intensity_ibp = key_values_in_excel["values"].iloc[7, 3]
    cement_emissions_intensity_reduction = cement_emissions_intensity_before - cement_emissions_intensity_after
    cement_emissions_intensity_difference_ibp = cement_emissions_intensity_ibp - cement_emissions_intensity_after

    # Helper functions
    def fmt_num(x, decimals=2):
        try:
            return f"{float(x):,.{decimals}f}"
        except Exception:
            return "0"

    def rel_phrase(diff, unit):
        """Return colored higher/lower/equal phrase."""
        try:
            d = float(diff)
        except Exception:
            d = 0.0
        if d < 0:
            return f"<b><font color='red'>{fmt_num(abs(d))} {unit} higher</font></b>"
        elif d > 0:
            return f"<b><font color='green'>{fmt_num(abs(d))} {unit} lower</font></b>"
        else:
            return "<b><font color='black'>equal to</font></b>"

    # Sentences
    text = (f"After applying your selected measures, your facility's final energy is reduced by "
        f"<b><font color='green'>{fmt_num(final_energy_reduction,1)} TJ</font></b> and is now "
        f"{rel_phrase(final_energy_difference_ibp, 'TJ')} than the International Best Practice value; "
        f"meanwhile, carbon dioxide emissions is reduced by "
        f"<b><font color='green'>{fmt_num(total_emissions_reduction,0)} tCO<sub>2</sub></font></b> and is now "
        f"{rel_phrase(total_emissions_difference_ibp, 'tCO<sub>2</sub>')} than the International Best Practice value.")

    return text

def df_to_table_part2(df: pd.DataFrame, title: str):
        styles = getSampleStyleSheet()

        df_display = df.copy().fillna("")

        # Paragraph style for table cells
        cell_style = ParagraphStyle(
            name="TableCell",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            wordWrap="CJK",   # enables wrapping
            alignment=1
        )
        header_style = ParagraphStyle(
            name="TableHeader",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            alignment=1
        )

        page_width, page_height = LETTER
        usable_width = page_width - 2 * 72  # 1-inch margins

        # Build table data with header row as Paragraphs
        data = [
            [Paragraph(str(col), header_style) for col in df_display.columns]
        ]
        for row in df_display.to_numpy():
            data.append([Paragraph(str(x), cell_style) for x in row])

        # Compute column widths (simple even split)
        ncols = max(1, len(df_display.columns))
        col_width = usable_width / ncols
        col_widths = [col_width] * ncols

        # Table with repeating header
        tbl = Table(data, colWidths=col_widths, repeatRows=1)

        # Style
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LINEABOVE", (0, 0), (-1, 0), 0.75, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 0.75, colors.black),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFBFB")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),

            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))

        # Title + table
        return [
            Paragraph(title, styles["Heading3"]),
            Spacer(1, 6),
            tbl,
            Spacer(1, 12),
        ]

def df_to_table_input_summary(df: pd.DataFrame, title: str):
        styles = getSampleStyleSheet()

        df_display = df.copy().fillna("")

        # Paragraph style for table cells
        cell_style = ParagraphStyle(
            name="TableCell",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            wordWrap="CJK",   # enables wrapping
            # center vertically
            spaceBefore=12,
            spaceAfter=12
        )
        header_style = ParagraphStyle(
            name="TableHeader",
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            alignment=1, # center
            spaceBefore=12,
            spaceAfter=12
        )

        page_width, page_height = LETTER
        usable_width = page_width - 2 * 72  # 1-inch margins

        # Build table data with header row as Paragraphs
        data = [
            [Paragraph(str(col), header_style) for col in df_display.columns]
        ]
        for row in df_display.to_numpy():
            data.append([Paragraph(str(x), cell_style) for x in row])

        # Compute column widths (simple even split)
        ncols = max(1, len(df_display.columns))
        col_width = usable_width / ncols
        col_widths = [col_width] * ncols

        # Table with repeating header
        tbl = Table(data, colWidths=col_widths, repeatRows=1)

        # Style
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F0F0F0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEABOVE", (0, 0), (-1, 0), 0.75, colors.black),
            ("LINEBELOW", (0, 0), (-1, 0), 0.75, colors.black),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CCCCCC")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FBFBFB")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))

        # Title + table
        return [
            Paragraph(title, styles["Heading3"]),
            Spacer(1, 6),
            tbl,
            Spacer(1, 12),
        ]

def generate_part1_report(self):
    data_dir = get_user_data_dir()
    graphs_dir = data_dir / "Graphs"

    OUTPUT_FILE_PATH = data_dir / f"Part1_BEST_Report_Output_{timestamp}.pdf"
    OUTPUT_FILE = str(OUTPUT_FILE_PATH)

    # Load Graphs
    graph_1 = graphs_dir / "Energy Benchmark.png"
    graph_2 = graphs_dir / "Direct Energy CO2 Emissions Benchmark.png"
    graph_3 = graphs_dir / "Indirect Energy CO2 Emissions Benchmark.png"
    graph_4 = graphs_dir / "Total CO2 Emissions Benchmark.png"
    graph_5 = graphs_dir / "energy benchmark by process.png"
    graph_6 = graphs_dir / "energy benchmark by process normalized.png"
    graph_7 = graphs_dir / "final energy consumption.png"
    graph_8 = graphs_dir / "primary energy consumption.png"
    graph_9 = graphs_dir / "energy cost.png"
    graph_10 = graphs_dir / "final energy by process.png"
    graph_11 = graphs_dir / "primary energy by process.png"
    graph_12 = graphs_dir / "energy cost by process.png"

    # Create PDF with ReportLab
    doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=LETTER)
    styles = getSampleStyleSheet()

    page_width, page_height = LETTER
    usable_width = page_width - 2 * 72  # 1-inch margins

    elements = []

    elements.append(Paragraph("Part 1 BEST Report ", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("The first half of the BEST Cement Tool analysis is completed. This report calculates and benchmarks your facility's energy consumption and carbon dioxide emissions with a hypothetical international best practice facility. Results are reported at both the facility level and process level. You can also find the energy and cost summaries of your facility and comparisons with the targets you set.", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("Final Energy Consumption Benchmark", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_1, width=usable_width, height=usable_width*0.56))
    elements.append(Spacer(1, 12)) # 12 is the vertical spacer, i.e.: how many blank lines after the content
    elements.append(Paragraph("Note: The international best practice value refers to the energy consumption of a hypothetical cement plant with the same quantities of raw material inputs, using the same type of kilns, producing the same type of cement, using the same type of fuel, and having the same steps, but using the best energy efficiency internationally for each step.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak()) # creates a new page

    elements.append(Paragraph("Direct Energy CO2 Emissions Benchmark", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_2, width=usable_width*0.75, height=usable_width*0.56*0.75)) # *0.75 because the graphs take up too much space
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Note 1: Direct energy emissions include carbon dioxide emissions from onsite fuel consumption for electricity generation and ceemnt production. \n Note 2: International best practice with different fuel refers to the direct energy emissions from a hypothetical facility with the same quantities of raw material inputs, using the same type of kilns, producing the same type of cement, and having the same steps as your facility, but using fuels with emission intensity of 0.00004 tCO2/MJ and the best energy efficiency internationally for each step.", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Indirect Energy CO2 Emissions Benchmark", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_3, width=usable_width*0.75, height=usable_width*0.56*0.75))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Note: Indirect emissions include carbon dioxide emissions from purchased elctricity only.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Total CO2 Emissions Benchmark", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_4, width=usable_width*0.75, height=usable_width*0.56*0.75))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Note 1: Total emissions include carbon dioxide emissions from onsite fuel consumption for electricity generation and ceemnt production, purchased electricity, and process emissions from calcination. It does not include other emissions such as those related to fuel production and transportation. \n Note 2: Process emissions are estimated solely based on the user input on clinker process emission intensity.", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Energy Benchmark by Process", styles['Heading2']))
    elements.append(Paragraph("Red = Your Facility; Green = International Best Practice Facility", styles['Normal']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_5, width=usable_width*0.9, height=usable_width*0.56*0.9))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Note: Additives preparation include additives crushing & grinding and additives drying; Kiln - machinery use includes preheater and clinker cooler; Kiln - clinker making includes precalciner and kiln.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Energy Benchmark by Process Normalized", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_6, width=usable_width, height=usable_width*0.56))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Note: A value of 1.0 indicates that your facility's final energy consumption for the specified process is in line with the hypothetical international best practice facility. A value greater than 1.0 indicates that your facility has higher energy consumption.", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Final Energy Consumption by Fuel", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_7, width=usable_width*0.75, height=usable_width*0.56*0.75))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Primary Energy Consumption by Fuel", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_8, width=usable_width*0.75, height=usable_width*0.56*0.75))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Note: This chart is for reference only. A simplified method is employed here to get primary energy consumption shares by fuel. All electricity consumption, whether purchased or generated onsite, are assumed to have conversion efficiencies of 30.5%.", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Energy Cost by Fuel", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_9, width=usable_width*0.75, height=usable_width*0.56*0.75))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Note: This chart is for reference only. A simplified method is employed here to calculate enegy cost shares by fuel. All electricity consumption is assumed to be from purchased electricity.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Final Energy by Process", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_10, width=usable_width, height=usable_width*0.44)) # it is 0.44, because figure size is (9, 4), which means height to width ratio should be 1:0.44
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Primary Energy by Process", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_11, width=usable_width, height=usable_width*0.44))
    elements.append(Paragraph("Note: This chart is for reference only. A simplified method is employed here to get primary energy consumption shares by process. All electricity consumption, whether purchased or generated onsite, are assumed to have conversion efficiencies of 30.5%.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Share of Energy Cost by Process", styles['Heading2']))
    elements.append(Spacer(1, 4))
    elements.append(Image(graph_12, width=usable_width, height=usable_width*0.44))
    elements.append(Paragraph("Note: This chart is for reference only. A simplified method is employed here to calculate enegy cost shares by process. All electricity consumption is assumed to be from purchased electricity.", styles['Normal']))
    elements.append(Spacer(1, 12))

    try:
        doc.build(elements)
    except Exception as e:
        print("PDF generation failed:", e)
        return

    QMessageBox.information(self, "Report Saved", f"Part 1 Report saved successfully.\nAfter review, please continue with Part 2. \nPlease find your files here: {data_dir}")
    open_pdf(OUTPUT_FILE)

def generate_part_2_report(self):

    filename="Saved_BEST_Report_Progress.json"
    data_dir = get_user_data_dir()
    json_folder = data_dir / "Saved Progress"

    graphs_dir = data_dir / "Graphs"

    OUTPUT_FILE_PATH = data_dir / f"BEST_Report_Part2_{timestamp}.pdf"
    OUTPUT_FILE = str(OUTPUT_FILE_PATH)

    # graph_1 = graphs_dir / "Energy Benchmark.png"
    # graph_2 = graphs_dir / "Direct Energy CO2 Emissions Benchmark.png"
    # graph_3 = graphs_dir / "Indirect Energy CO2 Emissions Benchmark.png"
    # graph_4 = graphs_dir / "Total CO2 Emissions Benchmark.png"
    # graph_5 = graphs_dir / "emissions waterfall.png"
    # graph_6 = graphs_dir / "energy waterfall.png"
    # graph_7 = graphs_dir / "abatement cost.png"

    graph_1 = graphs_dir / "energy benchmark after measures.png"
    graph_2 = graphs_dir / "direct energy co2 emissions benchmark after measures.png"
    graph_3 = graphs_dir / "indirect energy co2 emissions benchmark after measures.png"
    graph_4 = graphs_dir / "total co2 emissions benchmark after measures.png"
    graph_5 = graphs_dir / "energy waterfall.png"
    graph_6 = graphs_dir / "emissions waterfall.png"
    graph_7 = graphs_dir / "abatement cost.png"


    # Load Excel (all sheets)
    excel_file_path_1 = json_folder / "key_values_in_excel.xlsx"
    key_values_in_excel = pd.read_excel(excel_file_path_1, sheet_name=None)
    
    excel_file_path_2 = json_folder / "finance_key_values_in_excel.xlsx"
    finance_key_values_in_excel = pd.read_excel(excel_file_path_2, sheet_name=None)
    
    excel_file_path_3 = json_folder / "abatement_cost.xlsx"
    abatement_cost_in_excel = pd.read_excel(excel_file_path_3, sheet_name=None)

    # Create PDF with ReportLab
    doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=LETTER)
    styles = getSampleStyleSheet()

    page_width, page_height = LETTER
    usable_width = page_width - 2 * 72  # 1-inch margins

    elements = []

    elements.append(Paragraph("BEST Report ", styles['Title']))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("The BEST Cement Tool analysis is completed. This report compares the energy consumption and carbon dioxide emissions of your facility before and after applying the measures you selected. The impacts of each measure category on final energy consumption and carbon dioxide emissions are plotted in the waterfall charts. The abatement cost for each measure is indicated in the marginal abatement cost curve.", styles['Normal']))
    elements.append(Spacer(1, 12))

    auto_text = get_auto_text(key_values_in_excel)
    # add paragraph below
    elements.append(Paragraph(auto_text, styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Key Performance Values", styles['Heading2']))

    for sheet_name, df in key_values_in_excel.items():
        df.columns = ["Performance Metric", "Your facility before applying measures", "Your facility after applying measures", "International Best Practice"]

        elements.extend(df_to_table_part2(df, ""))
        elements.append(Spacer(1, 12))

    for sheet_name, df in finance_key_values_in_excel.items():
        df.columns = ["Financial Metric", "Values"]

        elements.extend(df_to_table_part2(df, ""))
        elements.append(Spacer(1, 12))

    
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Energy Benchmark", styles['Heading2']))
    elements.append(Image(graph_1, width=usable_width*.75, height=usable_width*.75*0.56))

    elements.append(Paragraph("Note: The international best practice value refers to the energy consumption of a hypothetical cement plant with the same quantities of raw material inputs, using the same type of kilns, producing the same type of cement, using the same type of fuel, and having the same steps as your facility, but using the best energy efficiency internationally for each step. It does not include the effects of any mitigation measures applied", styles['Normal']))
    elements.append(Spacer(1, 12))    

    elements.append(Paragraph("Direct Energy CO2 Emissions Benchmark", styles['Heading2']))
    elements.append(Image(graph_2, width=usable_width*.75, height=usable_width*.75*0.56))

    elements.append(Paragraph("Note 1: Direct energy emissions include carbon dioxide emissions from onsite fuel consumption for electricity generation and ceemnt production. \n Note 2: International best practice with different fuel refers to the direct energy emissions from a hypothetical facility with the same quantities of raw material inputs, using the same type of kilns, producing the same type of cement, and having the same steps as your facility, but using fuels with emission intensity of 0.00004 tCO2/MJ and the best energy efficiency internationally for each step. It does not include the effects of any mitigation measures applied.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Indirect Energy CO2 Emissions Benchmark", styles['Heading2']))

    elements.append(Image(graph_3, width=usable_width*.75, height=usable_width*.75*0.55)) # the aspect ratio here is 9 x 5 rather than 7 x 4 in other cases

    elements.append(Paragraph("Note: Indirect emissions include carbon dioxide emissions from purchased elctricity only.", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Total CO2 Emissions Benchmark", styles['Heading2']))

    elements.append(Image(graph_4, width=usable_width*.75, height=usable_width*.75*0.56))

    elements.append(Paragraph("Note 1: Total emissions include carbon dioxide emissions from onsite fuel consumption for electricity generation and ceemnt production, purchased electricity, and process emissions from calcination. It does not include other emissions such as those related to fuel production and transportation. \n Note 2: Process emissions are estimated solely based on the user input on clinker process emission intensity.", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Final Energy Reduction by Measurement Category", styles['Heading2']))

    elements.append(Image(graph_5, width=usable_width*.75, height=usable_width*.75*0.71)) # *0.71, because the aspect ratio of the graph is 700 x 500, (5/7 = 0.71)

    elements.append(Paragraph("EE = Energy Efficiency; DT = Other Technologies", styles['Normal']))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Total Carbon Dioxide Emissions Reduction by Measurement Category", styles['Heading2']))

    elements.append(Image(graph_6, width=usable_width*.75, height=usable_width*.75*0.71))

    elements.append(Paragraph("EE = Energy Efficiency; FS = Fuel Switching; RE = Renewable Electricity; DT = Other Technologies", styles['Normal']))
    elements.append(Spacer(1, 12))
    elements.append(PageBreak())

    elements.append(Paragraph("Marginal Abatement Cost Curve", styles['Heading2']))
    elements.append(Paragraph("Red = Energy efficiency measures; Blue = Other measures", styles['Normal']))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("EE = Energy Efficiency; DT = Other Technologies", styles['Normal']))
    elements.append(Image(graph_7, width=usable_width*.75, height=usable_width*.75*0.66))
    elements.append(Spacer(1, 4))
    
    for sheet_name, df in abatement_cost_in_excel.items():
        df.columns = ["Measure Index (from right to left)", "Measure", "Abatement Cost ($/tCO2)", "Emission Reduction Potential (tCO2)", "Measure Type"]

        elements.extend(df_to_table_part2(df, ""))
        elements.append(Spacer(1, 12))


    elements.append(Paragraph("Note 1: A discount rate of 9% and a project lifetime of 20 years are applied for calculating the abatement cost for each measure. The salvage value after the completion of the project lifetime is assuemd to be zero. \n Note 2:  The emission reduction potential of each measure reflects the contribution of the measure in the context when all measures selected are also applied, which lowers the overall emissions available for reduction. \n Note 3: Fuel switching and onsite renewable energy generation measures are not included here.", styles['Normal']))
    # Wrong: # The cumulative carbon dioxide emission reduction in the marginal abatement cost graph may nt equal the calculated total carbon dioxide emission reduction after measures above. This because in the calculations above, the energy and emissions available for reduction decrease with every measure applied. Meanwhile, in the marginal abatement cost graph, each measure's abatement cost is evaluated individually without any other measure applied.
    elements.append(Spacer(1, 12))

    try:
        doc.build(elements)
    except Exception as e:
        print("PDF generation failed:", e)
        return

    return OUTPUT_FILE
    

def generate_report_reportlab(self):
    
    # Not used. Originally planned to add abatement cost Excel to the report
    data_dir = get_user_data_dir()
    json_folder = data_dir / "Saved Progress"
    
    # Load Excel (all sheets)
    excel_file_path_1 = json_folder / "measures_output_in_excel.xlsx"
    excel_file_dummy = pd.ExcelFile(excel_file_path_1)
    list_of_sheet_names = excel_file_dummy.sheet_names
    EE_measure_in_excel_dict = {}
    for sheet in list_of_sheet_names:
        EE_measure_in_excel_dict[sheet] = pd.read_excel(excel_file_path_1, sheet_name=sheet)
        #EE_measure_in_excel_dict[sheet] = EE_measure_in_excel_dict[sheet].rename(columns={'Unnamed: 0': 'Measure'}, inplace=False)

    print("List of sheet names:")
    print(list_of_sheet_names)
    print(EE_measure_in_excel_dict)

    for sheet in EE_measure_in_excel_dict.keys():
        print(type(EE_measure_in_excel_dict[sheet]))

        
    filename="Saved_BEST_Report_Progress.json"
    OUTPUT_FILE_PATH = data_dir / f"User_Input_Summary_{timestamp}.pdf"
    OUTPUT_FILE = str(OUTPUT_FILE_PATH)

    excel_file_path_1 = json_folder / "report_in_excel.xlsx"
    report_in_excel_sheets = pd.read_excel(excel_file_path_1, sheet_name=None) 

    # Create PDF with ReportLab
    doc = SimpleDocTemplate(OUTPUT_FILE, pagesize=LETTER)
    styles = getSampleStyleSheet()

    page_width, page_height = LETTER
    usable_width = page_width - 2 * 72  # 1-inch margins

    elements = []

    elements.append(Paragraph("BEST Report ", styles['Title']))
    elements.append(Spacer(1, 12))
    # add paragraph below
    """
    if 
        elements.append(Paragraph("Quick assessment is selected.", styles['Normal']))
    else:
        elements.append(Paragraph("Detailed assessment is selected.", styles['Normal']))
    
    # EE measure evaluation selection
    from utils.save_progress import get_user_data_dir 
    data_dir = get_user_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    json_folder = data_dir / "Saved Progress"
    json_folder.mkdir(parents=True, exist_ok=True)
    
    with open(json_folder / "evaluate_EE_only.json", "r") as f:
        evaluate_EE_only = json.load(f)  
            
    if evaluate_EE_only != "Yes":
        elements.append(Paragraph("Only energy efficiency measures are evaluated.", styles['Normal']))
    else:
        elements.append(Paragraph("All measures are evaluated.", styles['Normal']))
    """
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("User Input and Calculations Summary", styles['Heading2']))

    for sheet_name, df in report_in_excel_sheets.items():
        # remove first row
        df = df.iloc[1:]
        df.columns = ["Field", "Value"]
        # add first sheet in excel file
        elements.extend(df_to_table_input_summary(df, sheet_name))
        elements.append(Spacer(1, 12))

    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Spacer(1, 12))

    # add table from excel
    # elements.extend(df_to_table(sheets_2, "Measures Output in Excel"))

    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Spacer(1, 12))

    # add table from excel
    # elements.extend(df_to_table(sheets_3, "Measures DT Output in Excel"))

    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Spacer(1, 12))
    #elements.append(Image(graph_path_process_co2_emissions_benchmark, width=600, height=300))

    elements.append(Spacer(1, 12))

    # elements.append(Paragraph("Calculations", styles['Heading2']))
    elements.append(Spacer(1, 12))
    # elements.append(Image(graph_path_process_co2_emissions_benchmark_normalized, width=600, height=300))
    elements.append(Paragraph(" ", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    """
    elements.append(Paragraph("Energy Efficiency Measures", styles['Heading2']))
    print("Print EE Measures tables")
    for sheet in list_of_sheet_names:
        print(EE_measure_in_excel_dict[sheet])
        #column_name = ["Measure", "Do you want to apply this measure?", "Potential Application", "Energy Consumption Share of Process", "Typical Energy Savings per Unit Mass", "Typical Investment per Unit Mass", "Typical Invesment per Unit Energy Saved", "Total Energy Savings Share", "Total Energy Savings Absolute", "Total Investment", "Payback Period", "Energy Type", "Process", "Abatement Cost", "Total Emission Reduction", "Total Emission Reduction - Direct", "Total Emission Reduction - Indirect"]
        column_name_index = 0
        for sheet_name, df in EE_measure_in_excel_dict[sheet].items():
            #df.columns = ["Measure", "Do you want to apply this measure?", "Potential Application", "Energy Consumption Share of Process", "Typical Energy Savings per Unit Mass", "Typical Investment per Unit Mass", "Typical Invesment per Unit Energy Saved", "Total Energy Savings Share", "Total Energy Savings Absolute", "Total Investment", "Payback Period", "Energy Type", "Process", "Abatement Cost", "Total Emission Reduction", "Total Emission Reduction - Direct", "Total Emission Reduction - Indirect"]
            print(df)
            print(sheet_name)

            if isinstance(df, pd.Series):
                # Force the Series into a DataFrame. 
                # We give it a temporary name, which will be overwritten by NEW_COLUMNS later.
                df = df.to_frame(name=column_name[column_name_index]) 
                print(f"INFO: Converted Series to DataFrame for sheet: {sheet_name}")
                
                column_name_index += 1      

           
            elements.extend(df_to_table_part2(df, ""))
            elements.append(Spacer(1, 12))
            """
    try:
        doc.build(elements)
    except Exception as e:
        print("PDF generation failed:", e)
        return

    print(f"PDF report generated as '{OUTPUT_FILE}'")
    return OUTPUT_FILE

def final_report_pdf(self):
    data_dir = get_user_data_dir()
    part2_report = generate_part_2_report(self)
    user_summary_report = generate_report_reportlab(self)

    QMessageBox.information(self, "Report Saved", f"Reports saved successfully.\nPlease find your files here: {data_dir}")
    
    QApplication.quit()
    open_pdf(user_summary_report)
    open_pdf(part2_report)

    print(f"PDF report generation successful")