from ingesting_engine import IngestingEngine
from processing_engine import ProcessingEngine
from recommending_engine import RecommendingEngine
import os
from pprint import pprint
import time
import tkinter as tk
import tkinter.filedialog
from ttkthemes import ThemedTk
import sys

class StdoutRedirector(object):
    ''' https://stackoverflow.com/questions/18517084/how-to-redirect-stdout-to-a-tkinter-text-widget '''
    def __init__(self,text_widget):
        self.text_space = text_widget

    def write(self,string):
        self.text_space.insert('end', string)
        self.text_space.see('end')

    def flush(self):
        # hey, this one is on me
        pass

class GraceApp:

    def __init__(self):
        self.root = ThemedTk(theme='adapta')
        self.root.configure(bg='white')
        self.root.title('GRACE')

        self.frm_master = tk.Frame(
            self.root,
            background='white'
        )
        self.frm_master.pack(
            fill='both',
            expand=True,
            padx=20,
            pady=20
        )
        # vars
        self.ent_folder_browser_str = tk.StringVar()
        self.ent_folder_browser_str.set('')
        self.ent_job_description_str = tk.StringVar()
        self.ent_job_description_str.set('')

        self.lbl_app_name = tk.Label(
            master=self.frm_master,
            text='GRACE',
            background='white',
            relief='raised',
            borderwidth=1
        )
        self.btn_restart_app = tk.ttk.Button(
            master=self.frm_master,
            text='Reiniciar',
            command=self.restart_app
        )
        # resume folder
        self.lbl_folder_browser = tk.ttk.Label(
            master=self.frm_master,
            text='Pasta com currículos',
            background='white',
            relief='raised',
            borderwidth=1,
            anchor='center'
        )
        self.ent_folder_browser = tk.ttk.Entry(
            master=self.frm_master,
            state=tk.DISABLED,
            textvariable=self.ent_folder_browser_str
        )
        self.btn_folder_browser = tk.ttk.Button(
            master=self.frm_master,
            text='Procurar',
            command=self.get_resume_folder
        )
        # job description file
        self.lbl_job_description = tk.ttk.Label(
            master=self.frm_master,
            text='Descrição da vaga',
            background='white',
            relief='raised',
            borderwidth=1,
            anchor='center'
        )
        self.ent_job_description = tk.ttk.Entry(
            master=self.frm_master,
            state=tk.DISABLED,
            textvariable=self.ent_job_description_str
        )
        self.btn_job_description = tk.ttk.Button(
            master=self.frm_master,
            text='Procurar',
            command=self.get_job_description_file
        )
        # process button
        self.btn_process = tk.ttk.Button(
            master=self.frm_master,
            text='Processar',
            command=self.hammer_time
            # command=self.hammer_time_test
        )
        # log output
        self.txt_log_output = tk.Text(
            master=self.frm_master,
            # state=tk.DISABLED,
            height=15,
            relief='solid'
        )
        sys.stdout = StdoutRedirector(self.txt_log_output)

        # grid aligns
        self.lbl_app_name.grid(
            row=0, column=2,
            columnspan=3, sticky='ns',
            ipadx=5, ipady=5
        )
        self.btn_restart_app.grid(row=3, column=1, sticky='ns')

        self.lbl_folder_browser.grid(
            row=1, column=1,
            padx=5, pady=5,
            ipadx=5, ipady=5,
            sticky='ns'
        )
        self.ent_folder_browser.grid(
            row=1, column=2,
            columnspan=3, sticky='nsew',
            padx=5, pady=5
        )
        self.btn_folder_browser.grid(row=1, column=5)
        
        self.lbl_job_description.grid(
            row=2, column=1,
            padx=5, pady=5,
            ipadx=5, ipady=5, 
            sticky='ns'
        )
        self.ent_job_description.grid(
            row=2, column=2,
            columnspan=3, sticky='nsew',
            padx=5, pady=5
        )
        self.btn_job_description.grid(row=2, column=5)

        self.btn_process.grid(row=3, column=2, columnspan=3, sticky='ns')

        self.txt_log_output.grid(
            row=4, column=1,
            rowspan=3, columnspan=5,
            sticky='ew',
            padx=5, pady=5    
        )

    def print_name(self):
        print('+-----------------+')
        print('|GRACE Version 0.1|')
        print('+-----------------+')
        time.sleep(1)

    def restart_app(self):
        ''' Restarts the entire script script '''
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def start_engines(self, resume_file_extension, lang):
        self.ingesting = IngestingEngine(resume_file_extension, verbose=1)
        self.processing = ProcessingEngine(lang)
        self.recommending = RecommendingEngine()

    def get_resume_folder(self):
        self.resume_folder = tk.filedialog.askdirectory()
        self.ent_folder_browser_str.set(self.resume_folder[-30:])

    def get_job_description_file(self):
        self.job_description_file = tk.filedialog.askopenfilename()
        self.ent_job_description_str.set(self.job_description_file[-30:])

    def hammer_time(self):
        self.start_engines('pdf', 'en')
        # ingesting
        print('\nIngesting')
        raw_job_description = self.ingesting.load_job_description(self.job_description_file)
        raw_resumes = self.ingesting.process_folder(self.resume_folder)

        # processing
        print('\nProcessing')
        self.processing.load_job_description(raw_job_description)
        self.processing.load_resumes(raw_resumes)
        
        job_description = self.processing.process_job_description()
        resumes = self.processing.process_resumes()
        
        # recommending
        print('\nRecommending')
        self.recommending.load_job_description(job_description)
        self.recommending.load_resumes(resumes)

        scores = self.recommending.run_steps()
        final_scores = self.recommending.get_scores()
        best_five = self.recommending.get_five_best_scores()
        self.show_recommendations(best_five)

    def show_recommendations(self, best_five):
        lbl_recommendation = tk.ttk.Label(
            master=self.frm_master,
            text='Melhores currículos'
        )
        lbl_recommendation.grid(
            row=8, column=2,
            padx=5, pady=5,
            ipadx=5, ipady=5,
            columnspan=3, sticky='ns'
        )

        self.command_btn_open_resume = []
        for col, recommendation in enumerate(best_five):
            self.command_btn_open_resume.append(recommendation)
            btn = tk.ttk.Button(
                master=self.frm_master,
                text=col+1,
                command=lambda c=col: self.open_resume(c)  # open resume
            )
            btn.grid(
                row=9, column=col+1,
                padx=5, pady=5,
                sticky='ns'
            )

    def open_resume(self, resume_n):
        # print(resume_n)
        os.startfile(self.command_btn_open_resume[resume_n])

    def hammer_time_test(self):
        print('This is not a test of the emergency broadcast system')


if __name__ == '__main__':
    # raw_resumes = os.path.join('Resume&Job_Description\Original_Resumes', '')
    # raw_job_descriptions = 'Resume&Job_Description\Job_Description\oaktree.txt'
    
    # g = GraceApp()
    # g.print_name()
    # g.start_engines('pdf', 'en')

    # # ingesting
    # print('\nIngesting')
    # resumes = g.ingesting.process_folder(raw_resumes)
    # job_description = g.ingesting.load_job_description(raw_job_descriptions)
    # # processing
    # print('\nProcessing')
    # g.processing.load_resumes(resumes)
    # g.processing.load_job_description(job_description)

    # processed_resumes = g.processing.process_resumes()
    # processed_job_description = g.processing.process_job_description()
    # # recommending
    # print('\nRecommending')
    # g.recommending.load_resumes(processed_resumes)
    # g.recommending.load_job_description(processed_job_description)
    # g.recommending.run_steps()
    # final_scores = g.recommending.get_scores()
    # pprint(final_scores)
    g = GraceApp()
    g.root.mainloop()
