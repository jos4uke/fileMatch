#/usr/bin/python2.7
#-*- coding: cp1251 -*-
#-*- coding: iso-8859-15 -*-
#-*- coding: utf-8 -*-

#///////////////////////////////////////////////////////////////////////
__author__ = "BEN HASSINE Najla(Najla.Ben-Hassine@versailles.inra.fr)"#/
__version__ = "1.0"				                      #/
__copyright__ = "Copyright (c) 2013-2014 BHN"                         #/
__license__ = "GROUPE DEV IJPB"			                      #/
#///////////////////////////////////////////////////////////////////////


"""
VERSION PYTHON UTILISEE:  Python 2.7.3 (64-bit)

PROGRAMME : MERGE DE N FICHIER .TXT (FICHIERS DE REVE POUR SNPEFF VERSION (snpEff_3_0))

MODULE : TRAITEMENT DE N FICHIER

"""


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- IMPORT DE LA BIBLIOTHEQUE  -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--DEBUT
#Bibliotheque systeme
import sys
import os
import glob
import getopt
import commands
import shutil

#Bibliotheque itertools: eficient iterator for loops
import itertools

#Gestion du log
import warnings
import logging
import logging.config
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- IMPORT DE LA BIBLIOTHEQUE  -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--FIN



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- CONFIGURATION -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--DEBUT

#___ FORMATAGE DU FICHIER LOG  --------------------------------------------------------------
def log_report(LOG_FILE_NAME):
	#**** FORMATAGE DU LOG ***
	logging.basicConfig(
		level=logging.DEBUG,
                format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
		datefmt='%m/%d/%Y %I:%M:%S %p',
                filename=LOG_FILE_NAME,
                filemode='w')

#___ FONCTION D AIDE --------------------------------------------------------------
def help_mergeDreamFile_script():
	print "**************"
	print  "H E L P  :"
	print "**************"
	print  " usage : ./fileMatch <DIR_IN> <DIR_OUT> <F1> <F2> ... <Fn> <-A>"
	print  " -h    : YOU NEED TWO FILES AT LEAST IN THE INPUT DIR "

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- CONFIGURATION -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--FIN



#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TEST AVANT TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--DEBUT
#___ TEST DE VERIFICATION DU NOMBRE DES ARGUMENTS  -------------------------------------------------
def verif_arg(argv):
	""" ****  FONCTION :  ****  \n\tverif_arg_nbr : VERIFICATION DES ARGUMENT """
    	#print sys.argv
    	if  (len(sys.argv) <= 1):	
    		help_mergeDreamFile_script()
    		sys.exit()
   	elif (len(sys.argv) == 2) and (sys.argv[1] == "-h"):
   	    	help_mergeDreamFile_script()
    		#sys.exit()
#		if sys.argv[1] == "-h":
#			help_dreamFileMaker_script()
#			sys.exit()
#		elif ".vcf" in sys.argv[1]:
#			#print 'Input VCF file is : ', sys.argv[1]
#			return  sys.argv[1]
#		elif ".vcf" not in sys.argv[1]:
#			print 'Input file : '+ sys.argv[1]+' IS NOT A .vcf'
#   	elif len(sys.argv) == 3:
#		if sys.argv[1] == "-h" and sys.argv[2] == "log_report" :
#			print log_report.__doc__
#		elif sys.argv[1] == "-h" and sys.argv[2] == "verif_arg_nbr" :
#			print verif_arg_nbr.__doc__
	return argv

#___ TEST NOMBRE DE FICHIER DANS LE REPERTOIRE D ENTREE -------------------------------------------------
def countFileNbr_repIn(REP_IN):
	filesIN = os.listdir(REP_IN)
	#print filesIN	
	nbr_filesIN = len(filesIN)
	#print nbr_filesIN	
	return nbr_filesIN

#___ TEST NOMBRE DE FICHIER DANS LE REPERTOIRE D ENTREE -------------------------------------------------
def countLineNbr_repIn(FileIn):
	listeLinesInFile=[]
	fin=open(FileIn,"r")
	listeLinesInFile=fin.readlines()
	fin.close()
	nbrLine = len(listeLinesInFile)
	return nbrLine
	
#___ VERIFIER LA VALIDITE DES FICHIERS D ENTREE ----------------------------------------------------------
def fileIN_validity(REP_IN):
	print "DEBUT ___ ETAPES DE VERIFICATION FICHIER "
	if countFileNbr_repIn(REP_IN) <= 1:
		msgCountFileIN = "[ERROR] :YOU NEED TO PUT 2 FILES AT LEAST."
		print msgCountFileIN
		logging.info(msgCountFileIN)
		check_validity_repIN = "ERROR"	
		print "FIN ___ ETAPES DE VERIFICATION FICHIER "
		return check_validity_repIN
	else:
		msgCountFileIN = "OK : YOU HAVE " + str(countFileNbr_repIn(REP_IN)) + " FILES TO MATCH"
		print msgCountFileIN
		logging.info(msgCountFileIN)
		check_validity_repIN = "OK"
		return check_validity_repIN

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TEST AVANT TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- FIN

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TEST APRES TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- DEBUT
#___ TEST NOMBRE DE COMBINAISON POSSIBLES  ------------------------------------------------------------------------
def count_combin_nbr(REP_IN):
	filesIN = os.listdir(REP_IN)
	msgCountCombinD = "DEBUT ___ ETAPES DE COMPTAGE DU NOMBRE DE COMBINAISONS"
	print msgCountCombinD 
	logging.info(msgCountCombinD)

	msgFileIN= "--- LISTE DES FICHIERS D ENTREE ---"
	print msgFileIN
	logging.info(msgFileIN)
	logging.info(str(filesIN))
	#print str(filesIN)
	
	#liste des combinaisons
	combinations = []
	for combination in itertools.combinations(filesIN, 2):
		combinations.append("___".join(str(i) for i in combination))
		
	msgFileINCombinList = "--- LISTE DES COMBINAISONS POSSIBLES  ---"
	print msgFileINCombinList
	logging.info(msgFileINCombinList)
	logging.info(str(combinations))
	print str(combinations)
	
	msgFileINCombinCount = "--- COMPTAGE DES COMBINAISONS POSSIBLES  ---"
	print msgFileINCombinCount
	logging.info(msgFileINCombinCount)
	logging.info(str(len(combinations)+1))
	print str(len(combinations)+1)
	msgCountCombinF = "FIN ___ ETAPES DE COMPTAGE DU NOMBRE DE COMBINAISONS"
	print msgCountCombinF 
	logging.info(msgCountCombinF)
	return combinations

#__ RECUPERATION DES LIGNES DE FICHIER DANS UNE LISTE
def readlines_fileIN(FileIn):
	listeLinesInFile=[]
	fin=open(FileIn,"r")
	listeLinesInFile=fin.readlines()
	fin.close()
	return listeLinesInFile

#__ EDITER UN FICHIER A PARTIR D UNE LISTE 
def write_line_inFile_fromList(listIN,fileOUt):
	fout = open(fileOUt,"w")
	for line in listIN:
		fout.write(line)
	fout.close()

#__ EDITER LE NOMBRE DE LIGNES DES FICHIERS OUTPUT
def list_all_files(REPORT_DIR_NAME):
	listOutPutFile= glob.glob(REPORT_DIR_NAME+'//*//*.txt') 
	print " ___ DEBUT DU COMPTAGE  ___ "
	logging.info( " ___ DEBUT DU COMPTAGE ___ ")

	print "Nombre de lignes par fichiers : "
	#logging.info("Nombre de lignes par fichiers : ")
	for f in listOutPutFile:
		#nbrLnInf = str(countLineNbr_repIn(f)) #+ " : " + f
		svg=sys.stdout 
		sys.stdout=open(REPORT_DIR_NAME+"/LogFile.log",'a')
		cmd = "wc -l " + f
		os.system(cmd)
		sys.stdout.close()
		sys.stdout=svg 
		#return nbrLnInf
	print " ___ FIN DU COMPTAGE ___ "
	#logging.info( " ___ FIN DU COMPTAGE ___ ")
	
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TEST APRES TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- FIN

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- DEBUT
#__TRAITEMENT DE CHAQUE COMBINAISON DE FICHIER
def trait_one_combination_file(fileCombinList,REP_IN,REPORT_DIR_NAME):
	print "FILES TO TREAT : " + str(fileCombinList)
	logging.info("FILES TO TREAT : " + str(fileCombinList))
	fileIN1 = readlines_fileIN(REP_IN+"/"+fileCombinList[0]+".txt")
	fileIN2 = readlines_fileIN(REP_IN+"/"+fileCombinList[1]+".txt")

	#__ REPERTOIRE DE LA COMBINAISON
	repCombin =  fileCombinList[0] + "___" + fileCombinList[1]
	
	#__ RECUPERATION DES COMMUNS ENTRE LES DEUX FICHIERS
	list_comm = sorted(list( set(fileIN1) & set(fileIN2)))

	#__ EDITER LE FICHIER DES COMMUNS DE LA COMBINAISON
	fileOUt = REPORT_DIR_NAME + "/" + repCombin + "/" + repCombin + "_comm.txt"
	print "PATH COMMUN FILE : "  + fileOUt
	logging.info("PATH COMMUN FILE : "  + fileOUt)
	write_line_inFile_fromList(list_comm,fileOUt)

	#__ RECUPERATION DES UNIQ POUR LE PREMIER FICHIER
	list_uniq1 = sorted(list(set(fileIN1) - set(fileIN2)))

	#__ EDITER LE FICHIER DES UNIQUE DU PREMIER FICHIER  DE LA COMBINAISON
	fileOUt1 = REPORT_DIR_NAME + "/" + repCombin + "/" + fileCombinList[0]+ "_uniq.txt"
	print "PATH uniq FILE : "  + fileOUt1
	logging.info( "PATH uniq FILE : "  + fileOUt1)
	write_line_inFile_fromList(list_uniq1,fileOUt1)

	#__ RECUPERATION DES UNIQ POUR LE DEUXIEME FICHIER
	list_uniq2 = sorted(list(set(fileIN2) - set(fileIN1)))

	#__ EDITER LE FICHIER DES UNIQUE DU PREMIER FICHIER  DE LA COMBINAISON
	fileOUt2 = REPORT_DIR_NAME + "/" + repCombin + "/" + fileCombinList[1]+ "_uniq.txt"
	print "PATH uniq FILE : "  + fileOUt2
	logging.info("PATH uniq FILE : "  + fileOUt2)
	write_line_inFile_fromList(list_uniq2,fileOUt2)

#___ RECUP DATA FROM COMBINATED FILES  ------------------------------------------------------------------------
def data_combinFile_recup(REP_IN,REPORT_DIR_NAME):
	#__COMPTAGE DU NOMBRE DE COMBINAISON ***
	listeFileCombinations = count_combin_nbr(REP_IN)
	#print listeFileCombinations
	#firstComb = listeFileCombinations[1]
			
	for combination in listeFileCombinations:
		print "DEBUT _________________________ TRAITEMENT DE LA COMBINAISON ___________________________________________"
		logging.info("DEBUT _________________________ TRAITEMENT DE LA COMBINAISON ___________________________________________")

		#__CREATION REP OUT
		nameCombinRep=combination.replace(".txt","")
		pathCombin=REPORT_DIR_NAME+"/"+nameCombinRep
		os.mkdir(pathCombin)
		
		print "CREATION DES REPERTOIRES CORRESPONDANT AUX COMBINAISONS : " + pathCombin
		logging.info( "CREATION DES REPERTOIRES CORRESPONDANT AUX COMBINAISONS : " + pathCombin)

		#__TRAITEMENT DE COMBINAISON
		#LISTE des deux fichies de la combinaison
		fileCombinList = combination.replace(".txt","").split("___")
		trait_one_combination_file(fileCombinList,REP_IN,REPORT_DIR_NAME)
		print "FIN _________________________ FIN DE TRAITEMENT DE LA COMBINAISON ___________________________________________"
		logging.info("FIN _________________________ FIN DE TRAITEMENT DE LA COMBINAISON ___________________________________________")

#COMBI DE TOUS LES FICHIERS 
def combin_all_file(REP_IN,REPORT_DIR_NAME,REP_OUT):
	print "DEBUT _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS ______________________________"
	logging.info("DEBUT _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS ______________________________")

	print "CREATION DU REPERTOIRES CORRESPONDANT A LA COMBINAISON DE TOUT LES FICHIERS " + REP_OUT
	logging.info( "CREATION DU REPERTOIRES CORRESPONDANT A LA COMBINAISON DE TOUT LES FICHIERS" + REP_OUT)

	listFileInRep =[]

	lineOfAllfiles =[]
	lineOfAllfiles_trie =[]

	listCommFile =[]
	listCommFile_Trie=[]

	listUniq=[]
	listUniq_Sorted =[]

	#Lister les fichiers du repertoire d entree
	listFileInRep = os.listdir(REP_IN)
	print "FILES TO TREAT : " + str(listFileInRep)
	logging.info("FILES TO TREAT : " + str(listFileInRep))
	
	#Recuperation des communs
	FileIn_ref = REP_IN +"/"+listFileInRep[0]
	listCommFile = readlines_fileIN(FileIn_ref)

	for fileIn in listFileInRep:	
		#ouverture du fichier
		fin=open(REP_IN +"/"+fileIn,"r")
		linesInfin = fin.readlines()
		#Recuperation de toutes les lignes dans une liste
		lineOfAllfiles = lineOfAllfiles + linesInfin
		listCommFile =  list(set(listCommFile) & set(linesInfin))
		fin.close()
	
	#print listCommFile
	#Recuperation des uniques des lignes en commun des fichiers
	listCommFile_Trie = sorted(set(listCommFile))
	#print listCommFile_Trie
	#print len(listCommFile_Trie)

	#Ecriture du fichier des communs
	foutcom = REP_OUT+"commAllFiles.txt"
	print "PATH COMMUN FILE : " + foutcom
	logging.info( "PATH COMMUN FILE : " + foutcom)
	write_line_inFile_fromList(listCommFile,foutcom)
	
	#Lecture des fichiers du repertoire	
	for i in range(len(listFileInRep)):
		finU=open(REP_IN +"/"+listFileInRep[i],"r")
		listlineU = finU.readlines()
		finU.close()	

		for fileIn in listFileInRep:	
			#ouverture du fichier
			fin=open(REP_IN +"/"+fileIn,"r")
			linesInfin = fin.readlines()
			listUniq =  list(set(listlineU) - set(linesInfin))

		#print listFileInRep[i]
		#print "liste " + listFileInRep[i] + " .uniq "
		#print listUniq
		fileName = listFileInRep[i].strip(".txt")
		foutUniq = REP_OUT+fileName+"_Uniq.txt"
		print "PATH UNIQ FILE : " + foutUniq
		logging.info( "PATH UNIQ FILE : " + foutUniq)
		write_line_inFile_fromList(sorted(listUniq),foutUniq)
	print "FIN _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS ___________________________________________"
	logging.info("FIN _________________________ TRAITEMENT DE DE L ENSEMBLE DES FICHIERS ___________________________________________")
	
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- FIN

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- MAIN -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
# ___ MAIN 
def main(argv):
	#___ TEST DE VERIFICATION DU NOMBRE DES ARGUMENTS  -------------------------------------------------
	verif_arg(argv)
	
#	#REPERTOIRE CONTENANT LES FICHIER D ENTREE
#	REP_IN = sys.argv[1].strip("/")
#	print "REPERTOIRE D ENTREE SPECIFIEE : " + REP_IN

#	#REPERTOIRE CONTENANT LES FICHIER DE SORTIE	
#	REPORT_DIR_NAME = sys.argv[2].strip("/")
#	print "REPERTOIRE DE SORTIE SPECIFIEE : " + REPORT_DIR_NAME

#	#__CREATION D UN FICHIER LOG ***
#	if os.path.exists(REPORT_DIR_NAME) is True:
#		shutil.rmtree(REPORT_DIR_NAME)
#		#os.system('rm -r' REPORT_DIR_NAME)
#		REPORT_DIR_NAME_Cmd = os.mkdir(REPORT_DIR_NAME)
#		LOG_FILE_NAME = REPORT_DIR_NAME + "/LogFile.log"
#		log_report(LOG_FILE_NAME)	
#	else:
#		REPORT_DIR_NAME_Cmd=os.mkdir(REPORT_DIR_NAME)
#		LOG_FILE_NAME= REPORT_DIR_NAME+"/LogFile.log"		
#		log_report(LOG_FILE_NAME)

#	#Creation d'un repertoire pour la combinaison de tous les fichiers.
#	REP_OUT = REPORT_DIR_NAME+"/AllFilesCombin/"
#	os.mkdir(REP_OUT)
#		
#	#__VERIFICATION DES ENTREES ***
#	logging.info("DEBUT ___ ETAPES DE VERIFICATION DES REPETOIRES")
#	CHECK= fileIN_validity(REP_IN)
#	
#	#__SUPPRESSION .APPLE
#	if os.path.exists(REP_IN+"/.AppleDouble") is True:
#		shutil.rmtree(REP_IN+"/.AppleDouble")
#	if CHECK == "OK":
#		print "OK : NUMBER OF FILES IS VALID."
#		logging.info("OK : NUMBER OF FILES IS VALID.")
#		logging.info("FIN ___ ETAPES DE VERIFICATION DES REPETOIRES")
#		print "FIN ___ ETAPES DE VERIFICATION FICHIER "
#		#__RECUPERATION DES DONNES DE LA COMBINAIS
#		#sdata_combinFile_recup(REP_IN,REPORT_DIR_NAME)

#		#FAIRE LA COMBINAISON DE TOUS LES FICHIERS
#		#combin_all_file(REP_IN,REPORT_DIR_NAME,REP_OUT)

#		#Creation rapport final
#		#list_all_files(REPORT_DIR_NAME)
#	else:
#		logging.info("[ERROR] : PLEASE SEE HELP FOR MORE INFORMATIONS")
#		help_mergeDreamFile_script()
#    	sys.exit()	
#	
		
if __name__ == "__main__":
	main(sys.argv[1:])


