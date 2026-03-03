from fpdf import FPDF
from fpdf.enums import XPos, YPos

title='ANALYSIS REPORT'

class PDF(FPDF):
    def header(self):
        """
        Creates a styled header for each PDF page.

        Displays the main report title centered at the top
        with custom border, background color, and text styling.

        Returns:
            None: Renders header directly onto the PDF page.
        """
        self.set_font('DejaVu','',16)
        
        #Adding title in centre
        title_w=self.get_string_width(title)
        doc_w=self.w
        self.set_x((doc_w-title_w)/2)
        
        self.set_draw_color(0, 80, 180) #blue
        self.set_fill_color(230, 230, 0) #yellow
        self.set_text_color(220, 50, 50) #red
        self.set_line_width(1)
        
        self.cell(title_w, 12, title, border=True, fill=True, align='C',
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(10)
        
    def footer(self):
        """
        Creates a footer with page numbering.

        Displays the page number centered at the bottom
        of each page in a subtle grey color.

        Returns:
            None: Renders footer directly onto the PDF page.
        """
        self.set_y(-10)
        self.set_font('DejaVu','',5)
        self.set_text_color(169,169,169)#grey
        self.cell(0,10,f'Page{self.page_no()}',align='C')
    
    #set title   
    def metric_title(self,mt_title):
        """
        Renders a section title for a specific metric.

        Args:
            mt_title (str): Title of the metric section.

        Returns:
            None: Writes the formatted title into the PDF.
        """
        self.set_font('DejaVu','',14)
        self.set_fill_color(200,220,255)
    
        self.cell(0,10,mt_title,new_x=XPos.LMARGIN, new_y=YPos.NEXT,fill=True)
        self.ln()
    
    #open text report
    def metric_body(self,name):
        """
        Reads and inserts a textual metric report into the PDF.

        Loads the corresponding text analysis file and writes
        its content in a justified format.

        Args:
            name (str): Path to the metric text report file.

        Returns:
            None: Embeds the text content into the PDF.
        """
        with open(name,'r',encoding='utf-8',errors='replace') as fh:
            txt=fh.read()
        
        self.set_font('DejaVu','',12)
        self.multi_cell(0, 5, txt, align='J')
        self.ln()
    
        self.set_font('DejaVu','',10)
        self.cell(0,5,'END OF REPORT',new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    
    def metric_chart(self,chart_name):
        """
        Inserts a chart image into the PDF.

        Args:
            chart_name (str): Path to the chart image file.

        Returns:
            None: Embeds the image into the PDF.
        """
        self.image(chart_name,x=10,w=self.w - 20)
        self.ln()
    
    
    
    
    def print_metric(self,mt_title,name,chart_list):
        """
        Generates a complete metric section in the PDF.

        Adds:
        - A new page with textual analysis
        - An optional visualization page with charts

        Args:
            mt_title (str): Metric section title.
            name (str): Path to the text report file.
            chart_list (list): List of chart image file paths.

        Returns:
            None: Writes the full metric section to the PDF.
        """
        self.add_page()
        self.metric_title(mt_title)
        self.metric_body(name)
        
        
        if chart_list:
            self.add_page()
            self.metric_title(f"{mt_title} - Visualizations")
            for chart in chart_list:
                self.image(chart, x=10, w=self.w - 20, h=110)
                self.ln(5)
     

        

if __name__=="__main__":
    
    #Object
    pdf=PDF('P','mm','A4')
    pdf.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
    pdf.set_auto_page_break(auto=True,margin=15)
    
    #printing user analysis
    pdf.print_metric(
    "User Metrics",
    "Outputs/Reports/user_analysis.txt",["Outputs/Charts/top_users.png","Outputs/Charts/success_rate.png"])
    
    #printing endpoint analysis
    pdf.print_metric(
    "Endpoint Analysis",
    "Outputs/Reports/endpoint_analysis.txt",["Outputs/Charts/slowest_endpoints.png","Outputs/Charts/avg_time_vs_success_rate.png"])
    
    #printing hourly analysis
    pdf.print_metric(
    "Hourly Patterns ",
    "Outputs/Reports/hourly_analysis.txt",["Outputs/Charts/hourly_traffic_pattern.png","Outputs/Charts/tot_requests and success_rate.png"])
    
    #printing daily analysis
    pdf.print_metric(
    "Daily Trends",
    "Outputs/Reports/daily_analysis.txt",["Outputs/Charts/Daily Trend with Errors.png"])
    
    #printing method analysis
    pdf.print_metric(
    "HTTP Methods",
    "Outputs/Reports/method_analysis.txt",["Outputs/Charts/Method Distribution.png","Outputs/Charts/Method_Success_vs_Error_Count.png"])
    
    pdf.output('Final_Report.pdf')
