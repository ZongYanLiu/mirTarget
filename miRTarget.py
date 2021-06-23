import argparse
import time
import pathlib
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from argparse import ArgumentParser

parser = ArgumentParser(description='miRTarget\nTools to combine psRNAtarget and MirTarSite\nPlease type in the full path of miRNA and transcriptome data for analyzing!')
parser.add_argument("miRNA", help="Full path of the microRNA fasta file.")
parser.add_argument("transcritome", help="Full path of the transcriptome fasta file.")
#parser.add_argument("-d", help="Full path of the degradome fasta file.", dest = "degra")

args = parser.parse_args()

with open(args.miRNA) as file, open(args.transcritome) as file:

	print("Full path to miRNA fasta file:", args.miRNA)
	print("Full path to transcriptome fasta file:", args.transcritome)
	#print("Full path to degradome fasta file:", args.degra)
	print("===============================================\nAnalyzing with psRNATarget...\n===============================================")

	options = Options()
	options.add_argument("window-size=1920x1080")
	#options.add_argument("--headless")     
	#options.add_argument("--disable-notifications")

	prefs = {"profile.default_content_settings.popups": 0, "download.default_directory": "%s/output/psRNATarget" %(pathlib.Path().absolute())}
	options.add_experimental_option("prefs",prefs)

	chrome = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=options)
	chrome.get("https://plantgrn.noble.org/psRNATarget/analysis?function=3")

	print("Successfully linked to psRNATarget!")

	chrome.find_element_by_id("srna").send_keys(args.miRNA)
	chrome.find_element_by_id("target").send_keys(args.transcritome)
	chrome.find_element_by_id("dosubmit2").click()

	time.sleep(3)
	print("Uploading your files...")

	a = [10,20,30,40,50,60,70,80,90]
	percent = int(0)
	while percent in range(99):
		percent = int(chrome.find_element_by_id("progressbar").get_attribute("aria-valuenow"))
		if percent in a :
			print(percent, "% uploaded!")
			time.sleep(2)
	print("Successfully uploaded all your sequencing data\npsRNATarget will start to analyze...")
	time.sleep(10)
	print ("You can find your result here:",chrome.current_url)
	number = chrome.current_url[56:]
	try:
		element = WebDriverWait(chrome, 360).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".glyphicon.glyphicon-download-alt")))
		print("Downloading psRNATarget result data...")	
		element.click()
	except:
		print("Thank you for patiently waiting...\nDownloading psRNATarget result data...")		
		chrome.get("https://plantgrn.noble.org/psRNATarget/data/%s?datatype=result" %(number))
	finally:
		file_path = r"%s/output/psRNATarget/psRNATargetJob-%s.txt" %(pathlib.Path().absolute(), number)
		while not os.path.exists(file_path):
			time.sleep(1)

		if os.path.isfile(file_path):
			print("Successfully analyzed by psRNATarget!")	
		chrome.quit()

	#print("===============================================\nAnalyzing with CleaveLand4...\n===============================================")
	#os.system("CleaveLand4.pl -e %s -u %s -n %s -o %s/output/CleaveLand4/ > %s/output/CleaveLand4/CleaveLand4_log.txt" %(args.degra , args.miRNA , args.target , pathlib.Path().absolute() , pathlib.Path().absolute()))


	print("===============================================\nAnalyzing with MirTarSite...\n===============================================")

	print("Converting results to fasta formate...")
	df = pd.read_csv("%s/output/psRNATarget/psRNATargetJob-%s.txt" %(pathlib.Path().absolute(), number), sep="\t", skiprows=[0])
	df["miRNA_aligned_fragment"] = df["miRNA_aligned_fragment"].str.replace('-', '')
	df["Target_aligned_fragment"] = df["Target_aligned_fragment"].str.replace('-', '')
	df.to_csv("%s/mirtarsite/example/interaction_pair.txt" %(pathlib.Path().absolute()), sep = "\t", index = False , header = False , columns=["miRNA_Acc." , "Target_Acc."])
	all_mir = r"%s/mirtarsite/example/all_mir.fa" %(pathlib.Path().absolute())
	all_site = r"%s/mirtarsite/example/all_site.fa" %(pathlib.Path().absolute())
	df.to_csv(all_mir, line_terminator = "\n>" , sep = "\n", index = False , header = False , columns=["miRNA_Acc.", "miRNA_aligned_fragment"] )
	df.to_csv(all_site, line_terminator = "\n>" , sep = "\n", index = False , header = False , columns=["Target_Acc.", "Target_aligned_fragment"] )

	with open(all_mir, "r") as f1, open(all_site, "r") as f2:
		first1 = f1.readline().strip()
		first2 = f2.readline().strip()
	with open(all_mir, "r") as d1, open(all_site, "r") as d2:
		list_of_lines1 = d1.readlines()
		list_of_lines2 = d2.readlines()
		list_of_lines1[0] = ">%s\n" %(first1)
		list_of_lines2[0] = ">%s\n" %(first2)
	with open(all_mir, "w") as d1, open(all_site, "w") as d2:
		d1.writelines(list_of_lines1)
		d2.writelines(list_of_lines2)
	with open(all_mir,"r") as fd1, open(all_site, "r") as fd2:
		d1=fd1.read()
		m1=d1.split("\n")
		s1="\n".join(m1[:-1])
		d2=fd2.read()
		m2=d2.split("\n")
		s2="\n".join(m2[:-1])
	with open(all_mir,"w+") as fd1, open(all_site, "w+") as fd2:
		for i in range(len(s1)):
			fd1.write(s1[i])
		for i in range(len(s2)):
			fd2.write(s2[i])
	if __name__=='__main__':
		os.system("python3 %s/mirtarsite/custom_predict.py %s/mirtarsite/state_dict/b16_lr0.001_embd100_rnnlayer1_rnnhidden100_drop0.3_ep47.pth %s/mirtarsite/example/all_mir.fa %s/mirtarsite/example/all_site.fa %s/mirtarsite/example/interaction_pair.txt %s/mirtarsite/example/output_result.txt --cuda True" %(pathlib.Path().absolute(), pathlib.Path().absolute(), pathlib.Path().absolute(), pathlib.Path().absolute(), pathlib.Path().absolute(), pathlib.Path().absolute()))
	df = pd.read_csv("%s/mirtarsite/example/out_V2.txt" %(pathlib.Path().absolute()), sep="\t")
	df.columns = ["microRNA", "target", "prediction"]
	pd.set_option('display.max_rows', None)
	with open("%s/output/mirRTarget_result_success.txt" %(pathlib.Path().absolute()), "w") as fd1, open("%s/output/miRTarget_result_false.txt" %(pathlib.Path().absolute()), "w") as fd2:
		print(df[df["prediction"] == 1], file = fd1)
		print(df[df["prediction"] == 0], file = fd2)
	print("Successfully analyze with miRTarget!\nYou can find your result at :%s/output/" %(pathlib.Path().absolute()))