from engines.ingesting_engine import IngestingEngine
from engines.processing_engine import ProcessingEngine
from engines.recommending_engine import RecommendingEngine
import argparse

def main(
    resume_dir_path: str,
    job_desc_file_path: str,
    language: str
    ):
    ingesting = IngestingEngine()
    processing = ProcessingEngine(language)
    recommending = RecommendingEngine()

    print('\nIngesting')
    raw_job_description = ingesting.load_job_description(job_desc_file_path)
    raw_resumes = ingesting.process_folder(resume_dir_path)

    # processing
    print('\nProcessing')
    processing.load_job_description(raw_job_description, is_pickle=False)
    processing.load_resumes(raw_resumes, is_pickle=False)
    
    job_description = processing.process_job_description()
    resumes = processing.process_resumes()
    
    # recommending
    print('\nRecommending')
    recommending.load_job_description(job_description)
    recommending.load_resumes(resumes)

    scores = recommending.run_steps()
    final_scores = recommending.get_scores()
    best_five = recommending.get_n_best_scores(n=5)
    recommending.copy_best_n_resumes(best_five, n=5)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GRACE CLI')

    parser.add_argument('resume_dir_path', type=str, help='pasta com os curriculos')
    parser.add_argument('job_desc_file_path', type=str, help='arquivo com a descricao da vaga')
    parser.add_argument('-l', '--language', type=str, help='linguagem a ser utilizada (padrao "pt-br")')

    args = parser.parse_args()
    main(
        args.resume_dir_path,
        args.job_desc_file_path,
        args.language
    )
