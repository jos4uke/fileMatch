#/usr/bin/python2.7
#-*- coding: cp1251 -*-
#-*- coding: iso-8859-15 -*-
#-*- coding: utf-8 -*-

#///////////////////////////////////////////////////////////////////////
__author__ = "BEN HASSINE Najla(Najla.Ben-Hassine@versailles.inra.fr)"#/
__version__ = "1.1"		                      	   	      #/
__date__= "20130808"		                      		      #/
__copyright__ = "Copyright (c) 2013-2014 BHN"                         #/
__license__ = "GROUPE DEV IJPB"			                      #/
#///////////////////////////////////////////////////////////////////////


"""
VERSION PYTHON UTILISEE:  Python 2.7.3 (64-bit)

PROGRAMME : MERGE DE N FICHIER .TXT (FICHIERS DE REVE POUR SNPEFF VERSION (snpEff_dev))

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
#___VARIABLE GLOABALE 
global LOG_FILE_NAME
global DATA_TABLE_FILE_NAME 
global DATA_MATRICE_VENN
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
	print  " usage : fileMatch <DIR_IN> <DIR_OUT> <F1> <F2> ... <Fn> <-A/-C/-Cn/-AC/-ACn>"
	print  " -h    : vous avez besoin de 2 fichiers .txt (au moins), pour faire le traitement."
	print  " Pour plus d'infos veuillez consulter le readme."
	print  	" ** l'outil peut etre lancer de deux façons: "
	print  "	1/ En specifiant une liste de fichiers."
	print  "	2/ Sans specifier une liste de fichiers."

	print  " ** La commande pour lancer l'outil en specifiant une liste de fichier : "
	print  "	cheminExecutable <Repertoire_dentree> <Repertoire_de_sortie> <file1.txt> <file2.txt>  -<Type_de_traitment> "

	print  " ** La commande pour lancer l'outil SANS SPECIFIE une liste de fichier : Tous les fichiers .txt du repertoire seront traites."
	print  "	cheminExecutable <Repertoire_dentree> <Repertoire_de_sortie>  -<Type_de_traitment> "

	print  " ** Trois types de traitements existent : "
	print  " -A : Traitement de l'ensemble de fichier. Un seul dossier sera cree en sortie : AllFilesCombin "
	print  " -C : Traitement des combinaisons de fichiers. Seuls les dossiers correspondant aux combinaisons de fichier 2 a 2 seront crees /  exp : file1___file2 "
	print  " -AC: C'est la combinaison des deux traitements precedents. Deux types de dossiers seront crees. Un dossier AllFilesCombin et les dossiers correspondant aux combinaisons. "
	print  " n: C'est le type de combinaison souhaitee : 2 pour 2a2, 3 pour 3a3, 4 pour 4a4, 5 pour 5a5."
	print  " NB: chaque dossier cree contient un fichier contenant les communs entre les fichiers, et un fichier pour chaque fichier traite, correspondant aux uniques de celui-ci."

	print  " ** Recommandations: "
	print  "	- Copier les donnees a traiter dans un nouveau repertoire qui sera le repertoire d'entree. "
	print  "	- Verifier la liste des fichiers contenu dans le repertoire d'entree (Des sorties .txt du pipeline mutdetect du type nomEchantillon_snpeff_snpsift_OneLineEff_DF.txt)"
	print  "	- Creation d'un repertoire de sortie en dehors du repertoire d'entree."
	print  "	- Verifier votre repertoire de sortie a chaque fois que vous lancer l'outil, pour ne pas ecraser des anciennes analyses."
	print  "	- Les fichiers passes en argument doivent imperativement appartenir au repertoire d'entree."

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- CONFIGURATION -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--FIN


#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TEST AVANT TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#--DEBUT
#___ TEST DE VERIFICATION DU NOMBRE DES ARGUMENTS  -------------------------------------------------
#___ TEST DE VERIFICATION 1er  ARGUMENT  -------------------------------------------------
def verif_arg1(argv,LOG_FILE_NAME):
	"""FONCTION :  ****  \n\tverif_arg1 : VERIFICATION DU PREMIER ARGUMENT """
	global listeFileExt
	listeFileExt= []
	#print sys.argv
	
   	if (len(sys.argv) <= 1) or (sys.argv[1] == "-h"):
			help_mergeDreamFile_script()
			#print sys.argv
			arg1_check ="OK"
			#EFFACER LE LOG_FILE_NAME
			os.system("rm " + LOG_FILE_NAME)
			return  arg1_check
			sys.exit()
	
	elif (len(sys.argv) > 1) and (sys.argv[1] != "-h"):
		print "\n__VERIFICATION DU 1er ARGUMENT : " + sys.argv[1]
		logging.info("\n__VERIFICATION DU 1er ARGUMENT : " + sys.argv[1])
		if str(os.path.isdir(sys.argv[1])) == "True":
			#liste de fichier disponibles dans le repertoire
			listFileRepIN = os.listdir(sys.argv[1])
			for fileInrep in listFileRepIN:
				if os.path.splitext(fileInrep)[1] == ".txt" :
						listeFileExt.append(fileInrep)
			if len(listeFileExt) >= 2 :
				print " [OK] : REPERTOIRE D ENTREEE VALIDE.\n\tPATH :  " + sys.argv[1] + "\n\tListe des fichiers disponibles :" 
				logging.info(" [OK] : REPERTOIRE D ENTREEE VALIDE.\n\tPATH :  " + sys.argv[1] + "\n\tListe des fichiers disponibles :")
				for fileInArg in listeFileExt:
					if  (str(os.path.isfile(sys.argv[1]+fileInArg))) =="True" :
						print fileInArg
						logging.info(fileInArg)

				#__VERIFICATION DES ENTREES ***
				CHECK= fileIN_validity(sys.argv[1])
	
				#__SUPPRESSION .APPLE
				if os.path.exists(sys.argv[1]+"/.AppleDouble") is True:
					shutil.rmtree(sys.argv[1]+"/.AppleDouble")
					os.system("rm " + ".DS_Store")
				if CHECK == "OK":
					print "\t[OK] : NOMBRE DE FICHIER VALIDE."
					logging.info("[OK] : NOMBRE DE FICHIER VALIDE")
					
				logging.info("FIN ___ ETAPES DE VERIFICATION DES REPETOIRES")
				print "FIN ___ ETAPES DE VERIFICATION FICHIER "
				
				arg1_check ="OK"
				return  arg1_check
			
			elif len(listeFileExt) < 2 :
				msgArg1Error= "[ERROR] : ARGUMENT NON VALIDE. DONNEZ UN REPERTOIRE D ENTREE VALIDE (contenant au moins deux fichiers .txt ) SVP."
				#print msgArg1Error
				logging.error(msgArg1Error)
				sys.stderr.write(msgArg1Error)
				arg1_check ="ERROR"			
				return  arg1_check

		elif str(os.path.isdir(sys.argv[1])) == "False":
			msgArg1Error2 = "[ERROR] : ARGUMENT NON VALIDE. DONNEZ UN REPERTOIRE D ENTREE VALIDE (contenant au moins deux fichiers .txt ) SVP."
			#print msgArg1Error2
			logging.error(msgArg1Error2)
			sys.stderr.write(msgArg1Error2)
			arg1_check ="ERROR"			
			return  arg1_check
	else:					
		msgArg1Error3 = "[ERROR] : ARGUMENT NON VALIDE. DONNEZ UN REPERTOIRE D ENTREE VALIDE (contenant au moins deux fichiers .txt ) SVP."
		#print msgArg1Error3
		logging.error(msgArg1Error3)
		sys.stderr.write(msgArg1Error3)
		arg1_check ="ERROR"			
		return  arg1_check
		
#___ TEST : FICHIER EN ARG APPARTIENNET AU REPERTOIRE D ENTREE  -------------------------------------------------	
def fileArgList(argv):
	global listFichierEnArg
	listFichierEnArg=[]
	#print listeFileExt
	#print sys.argv
	for arg in sys.argv:
		if (arg != sys.argv[0]) and (arg != sys.argv[1]) and (arg != sys.argv[2]) and (arg != sys.argv[len(sys.argv) -1]):
			listFichierEnArg.append(arg)
	#print listFichierEnArg
	
	print "\n__VERIFICATION DU 3ème ARGUMENT : Presence d'une liste de fichiers." 
	if len(listFichierEnArg) >= 2:
		print "VOUS AVEZ CHOISI DE TRAVAILLER AVEC UN SOUS ENSEMBLE DU FICHIER DU REPERTOIRE D ENTREE."
		for fileArg in listFichierEnArg:
			if fileArg in (os.listdir(sys.argv[1])):
				arg3_check_msg = " [OK] : LE FICHIER SPECIFE : " + fileArg + ", APPARTIENT AU REPERTOIRE D ENTREE.\n"
				print arg3_check_msg
				logging.info(arg3_check_msg)	
				arg3_check ="OK"			
			else:
				arg3_check_msg = " [ERROR] : LE FICHIER SPECIFE : " + fileArg + ", N APPARTIENT PAS AU REPERTOIRE D ENTREE. VEUILLEZ RECOMMENCER.\n"
				#print arg3_check_msg
				logging.error(arg3_check_msg)
				sys.stderr.write(arg3_check_msg)
				arg3_check ="ERROR"
		return arg3_check
				
	elif len(listFichierEnArg) == 1:
		arg3_check_msg = " [ERROR] : IL FAUT SPECIFIER AU MOINS DEUX FICHIERS APPARTIENT PAS AU REPERTOIRE D ENTREE.\n"
		#print arg3_check_msg
		logging.error(arg3_check_msg)
		sys.stderr.write(arg3_check_msg)
		arg3_check ="ERROR"
		return arg3_check
		
	else:
		arg3_check_msg = " [OK] : PAS DE LISTE DE FICHIERS EN ARG. TOUS LES FICHIERS DU REPERTOIRE D ENTREE SERONT TRAITES.\n"
		print arg3_check_msg
		arg3_check ="OK_withoutFilesList"
		logging.info(arg3_check_msg)
		return arg3_check
		
#___ TEST DE VERIFICATION 2eme ARGUMENT  -------------------------------------------------		
def verif_arg2(argv,LOG_FILE_NAME):
	"""FONCTION :  ****  \n\tverif_arg2 : VERIFICATION DU 2eme ARGUMENT """
	arg1_check = verif_arg1(argv,LOG_FILE_NAME)
	#print arg1_check
	if (len(sys.argv) > 2) and (arg1_check == "OK"):
		print "\n__VERIFICATION DU 2ème ARGUMENT : " + sys.argv[2]
		logging.info("\n__VERIFICATION DU 2ème ARGUMENT : " + sys.argv[2])
		
		#print str(os.path.exists(sys.argv[2]))
		#print str(os.path.isdir(sys.argv[2]))
		if (str(os.path.exists(sys.argv[2])) == "True") and (str(os.path.isdir(sys.argv[2])) == "True"):
			#pathname = os.path.dirname(sys.argv[2])
			print " [OK] : REPERTOIRE DE SORTIE EST VALIDE:\n\tPATH : " + os.path.abspath(sys.argv[2])
			logging.info(" [OK] : REPERTOIRE DE SORTIE EST VALIDE:\n\tPATH : " + os.path.abspath(sys.argv[2]))
			arg2_check ="OK"
			cmd_mv_log =  "mv " + LOG_FILE_NAME + " ./" + sys.argv[2].rstrip("/")+"/"
			os.system(cmd_mv_log)
			return  arg2_check
			
		elif (str(os.path.exists(sys.argv[2])) == "False") and (str(os.path.isdir(sys.argv[2])) == "False"): 
			print "[WARNING] : LE REPERTOIRE DE SORTIE SPECIFIEE : " + sys.argv[2] + " N EXSTE PAS. IL SERA CREE SOUS LE CHEMIN INDIQUE.\n" + os.path.abspath(sys.argv[2])
			logging.warning("[WARNING] : LE REPERTOIRE DE SORTIE SPECIFIEE : " + sys.argv[2] + " N EXSTE PAS. IL SERA CREE SOUS LE CHEMIN INDIQUE.\n" + os.path.abspath(sys.argv[2]))
			os.mkdir(sys.argv[2])
			cmd_mv_log =  "mv " + LOG_FILE_NAME + " ./" + sys.argv[2].rstrip("/")+"/"
			os.system(cmd_mv_log)
			
			print "[OK] : LE REPERTOIRE DE SORTIE EST CREE."
			logging.info("[OK] : LE REPERTOIRE DE SORTIE EST CREE.")
			arg2_check ="OK"
			return  arg2_check
			
	elif (len(sys.argv) > 1 and len(sys.argv) < 3) and sys.argv[1] != "-h" and sys.argv[1] != "" :
		msgErrArg2 =  "\n[ERROR] : LE REPERTOIRE DE SORTIE N'EST PAS SPECIFIE. VEUILLEZ RECOMMENCER.\n"
		#print msgErrArg2
		logging.error(msgErrArg2)
		sys.stderr.write(msgErrArg2)
		arg2_check ="ERROR"			
		return  arg2_check

	
#___ TEST DE VERIFICATION 3eme /dernier ARGUMENT  -------------------------------------------------		
def verif_lastArg(argv,LOG_FILE_NAME,DATA_TABLE_FILE_NAME,DATA_MATRICE_VENN):
	nbrComb=2
	"""FONCTION :  ****  \n\tverif_arg3 : VERIFICATION DU 3eme ARGUMENT """
	arg2_check = verif_arg2(argv,LOG_FILE_NAME)
	last_arg = str(sys.argv[len(sys.argv) -1]).upper()
	if (len(sys.argv) > 3) and (arg2_check == "OK") and (".txt" not in last_arg):
		print "\n__VERIFICATION DU 4ème ARGUMENT : " + sys.argv[len(sys.argv)-1]
		logging.info("\n__VERIFICATION DU 4ème ARGUMENT : " + sys.argv[len(sys.argv)-1])
		if last_arg == "-A" :
			print " [WARNING] : SEUL LE TRAITEMENT DE TYPE 1 SERA REALISE. VOIR LE README/HELP POUR PLUS D'INFOS.\n"
			logging.warning(" [WARNING] : SEUL LE TRAITEMENT DE TYPE 1 SERA REALISE. VOIR LE README/HELP POUR PLUS D'INFOS.\n")
			#Creation d'un repertoire pour la combinaison de tous les fichiers.
			REP_OUT_ALL = sys.argv[2].rstrip("/") +"/AllFilesCombin/"
			
			if str(os.path.isdir(REP_OUT_ALL)) == "False" : 
				os.mkdir(REP_OUT_ALL)
				#print "\tFICHIER LOG PATH : " + LOG_FILE_NAME
				#log_report(LOG_FILE_NAME)
				
			#SANS liste de fichiers en argument
			checkFileListe = fileArgList(argv)
			if checkFileListe == "OK_withoutFilesList" :
				#Faire le traitement pour tous ls fichiers du repertoire
				listFilesIn =listeFileExt
				print "DEBUT _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS ____________________________"
				logging.info("DEBUT _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS _____________________")
				combin_all_file(sys.argv[1],sys.argv[2].rstrip("/"),REP_OUT_ALL,DATA_TABLE_FILE_NAME,listFilesIn,DATA_MATRICE_VENN)
				print "FIN _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS ____________________________"
				logging.info("FIN _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS _____________________")

			#AVEC liste de fichier en argument
			elif checkFileListe == "OK" : 
				listFilesIn = listFichierEnArg
				combin_all_file(sys.argv[1],sys.argv[2].rstrip("/"),REP_OUT_ALL,DATA_TABLE_FILE_NAME,listFilesIn,DATA_MATRICE_VENN)
			return last_arg

		elif "-C" in last_arg :
			print "[WARNING] : SEUL LE TRAITEMENT DE TYPE 2 SERA REALISE. VOIR LE README/HELP POUR PLUS D'INFOS.\n"
			logging.warning("[WARNING] : SEUL LE TRAITEMENT DE TYPE 2 SERA REALISE. VOIR LE README/HELP POUR PLUS D'INFOS.\n")
			#Sans liste de fichiers en argument
			checkFileListe = fileArgList(argv)
			if checkFileListe == "OK_withoutFilesList" :
				#FAIRE LA COMBINAISON DE TOUS LES FICHIERS
				listFilesIn =listeFileExt
				recupTrai=last_arg
				if last_arg ==  "-C":
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,2,DATA_MATRICE_VENN)

				else:
					nbrComb=int(last_arg.replace("-C",""))
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,nbrComb,DATA_MATRICE_VENN)
						

			#AVEC liste de fichier en argument
			elif checkFileListe == "OK" : 
				listFilesIn = listFichierEnArg
				recupTrai=last_arg
				if last_arg ==  "-C":
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,2,DATA_MATRICE_VENN)

				else:
					nbrComb=int(last_arg.replace("-C",""))
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,nbrComb,DATA_MATRICE_VENN)
			return last_arg



		elif "-AC" in last_arg :
			print "[WARNING] : LES TRAITEMENTS DE TYPE 1+2 SERONT REALISES. VOIR LE README/HELP POUR PLUS D'INFOS.\n"
			logging.warning("[WARNING] : LES TRAITEMENTS DE TYPE 1+2 SERONT REALISES. VOIR LE README/HELP POUR PLUS D'INFOS.\n")

			#Creation d'un repertoire pour la combinaison de tous les fichiers.
			REP_OUT_ALL = sys.argv[2].rstrip("/") +"/AllFilesCombin/"
			
			if str(os.path.isdir(REP_OUT_ALL)) == "False" : 
				os.mkdir(REP_OUT_ALL)
				#print "\tFICHIER LOG PATH : " + LOG_FILE_NAME
				#log_report(LOG_FILE_NAME)
				
			#SANS liste de fichiers en argument
			checkFileListe = fileArgList(argv)
			if checkFileListe == "OK_withoutFilesList" :
				#Faire le traitement pour tous ls fichiers du repertoire
				listFilesIn =listeFileExt
				print "DEBUT _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS ____________________________"
				logging.info("DEBUT _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS _____________________")
				combin_all_file(sys.argv[1],sys.argv[2].rstrip("/"),REP_OUT_ALL,DATA_TABLE_FILE_NAME,listFilesIn,DATA_MATRICE_VENN)
				print "FIN _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS ____________________________"
				logging.info("FIN _________________________ TRAITEMENT DE LA COMBINAISON DE L ENSEMBLE DES FICHIERS _____________________")

			#AVEC liste de fichier en argument
			elif checkFileListe == "OK" : 
				listFilesIn = listFichierEnArg
				combin_all_file(sys.argv[1],sys.argv[2].rstrip("/"),REP_OUT_ALL,DATA_TABLE_FILE_NAME,listFilesIn,DATA_MATRICE_VENN)

			#Sans liste de fichiers en argument
			checkFileListe = fileArgList(argv)
			if checkFileListe == "OK_withoutFilesList" :
				#FAIRE LA COMBINAISON DE TOUS LES FICHIERS
				listFilesIn =listeFileExt
				if last_arg ==  "-AC":
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,nbrComb,DATA_MATRICE_VENN)

				else:
					nbrComb=int(last_arg.replace("-AC",""))
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,nbrComb,DATA_MATRICE_VENN)
						

			#AVEC liste de fichier en argument
			elif checkFileListe == "OK" : 
				listFilesIn = listFichierEnArg
				recupTrai=last_arg
				if last_arg ==  "-AC":
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,nbrComb,DATA_MATRICE_VENN)

				else:
					nbrComb=int(last_arg.replace("-AC",""))
					data_combinFile_recup(sys.argv[1],sys.argv[2].rstrip("/"),DATA_TABLE_FILE_NAME,listFilesIn,nbrComb,DATA_MATRICE_VENN)
			return last_arg

							
		else:
			logging.error("[ERROR] : SPECIFIEZ LE TYPE DE TRAITEMENT SVP. VOIR LE README/HELP POUR PLUS D'INFOS.\n")
			sys.stderr.write("[ERROR] : SPECIFIEZ LE TYPE DE TRAITEMENT SVP. VOIR LE README/HELP POUR PLUS D'INFOS.\n")
			return last_arg
			
	elif (len(sys.argv) < 4 and len(sys.argv) > 1 ) and sys.argv[1] != "-h" and sys.argv[1] != "":
		logging.error("[ERROR] : VOUS AVEZ OMIS AU MOINS UN ARGUMENT. VEUILLEZ RECOMMENCER.\n")
		sys.stderr.write("[ERROR] : VOUS AVEZ OMIS AU MOINS UN ARGUMENT. VEUILLEZ RECOMMENCER.\n")
		return last_arg
		
#___ TEST NOMBRE DE FICHIER DANS LE REPERTOIRE D ENTREE -------------------------------------------------
def countFileNbr_repIn(REP_IN):
	nbrFilelist=[]
	filesIN = os.listdir(REP_IN)
	for filename in filesIN:
		filename= filename.split(".")
		if filename[1] == "txt":
			nbrFilelist.append(filename)
	#print filesIN	
	nbr_filesIN = len(nbrFilelist)
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
def fileIN_validity(listeFileExt):
	REP_IN=listeFileExt
	print "\nDEBUT ___ ETAPES DE VERIFICATION DES FICHIERS "
	if countFileNbr_repIn(REP_IN) <= 1:
		msgCountFileIN = "\t[ERROR] :IL FAUT AU MOINS DE FICHIER POUR LE TRAITEMENT."
		print msgCountFileIN
		logging.info(msgCountFileIN)
		check_validity_repIN = "ERROR"	
		print "FIN ___ ETAPES DE VERIFICATION DES FICHIERS.\n"
		return check_validity_repIN
	else:
		msgCountFileIN = "\t[OK] : VOUS AVEZ " + str(countFileNbr_repIn(REP_IN)) + " FICHIERS A TRAITER."
		print msgCountFileIN
		logging.info(msgCountFileIN)
		check_validity_repIN = "OK"
		return check_validity_repIN

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TEST AVANT TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- FIN

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TEST APRES TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- DEBUT
#___ TEST NOMBRE DE COMBINAISON POSSIBLES  ------------------------------------------------------------------------
def count_combin_nbr(listeFileExt,nbrComb):
	filesIN = listeFileExt
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
	listCombinFormate=[]

	for combination in itertools.combinations(filesIN, nbrComb):
		combinations.append("___".join(str(i) for i in combination))

	for combin in combinations:
		 listCombinFormate.append(combin.replace("_snpeff_snpsift_OneLineEff_DF.txt",""))

	msgFileINCombinList = "--- LISTE DES COMBINAISONS POSSIBLES  ---"
	print msgFileINCombinList
	logging.info(msgFileINCombinList)
	logging.info(str(listCombinFormate))
	print str(listCombinFormate)
	
	msgFileINCombinCount = "--- COMPTAGE DES COMBINAISONS POSSIBLES  ---"
	print msgFileINCombinCount
	logging.info(msgFileINCombinCount)
	logging.info(str(len(combinations)))
	print str(len(combinations))
	msgCountCombinF = "FIN ___ ETAPES DE COMPTAGE DU NOMBRE DE COMBINAISONS"
	print msgCountCombinF 
	logging.info(msgCountCombinF)
	return listCombinFormate
	
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
def trait_one_combination_file(combin,REP_IN,REPORT_DIR_NAME):
	listFileInCombin=[]
	listFileInCombinSorted=[]
	listFilesC=combin.split("___")
	for fileC in listFilesC:
		#pathfileC = REP_IN.strip("/")+"/"+fileC+"_snpeff_snpsift_OneLineEff_DF.txt"
		pathfileC = fileC+"_snpeff_snpsift_OneLineEff_DF.txt"
		listFileInCombin.append(pathfileC)
	listFileInCombinSorted=sorted(set(listFileInCombin))
	print "FILES TO TREAT FOR : " + combin + "\n"+ str(listFileInCombinSorted)
	logging.info("FILES TO TREAT FOR : " + combin + "\n"+ str(listFileInCombinSorted))

	return listFileInCombinSorted
#___ RECUP DATA FROM COMBINATED FILES  ------------------------------------------------------------------------
def data_combinFile_recup(REP_IN,REP_OUT,DATA_TABLE_FILE_NAME,listFilesIn,nbrComb,DATA_MATRICE_VENN):
	#__COMPTAGE DU NOMBRE DE COMBINAISON ***
	listeFileCombinations = count_combin_nbr(listFilesIn,nbrComb)
	
	for combinI in listeFileCombinations :
		print "DEBUT ____________________ TRAITEMENT DE LA COMBINAISON "+combinI+"___________________________________________"
		logging.info("DEBUT _____________ TRAITEMENT DE LA COMBINAISON  "+combinI+"_________________________________")

		print "\tCREATION DU REPERTOIRE DE SORTIE DE LA COMBINAISON"
		logging.info("\tCREATION DU REPERTOIRE DE SORTIE DE LA COMBINAISON")

		pathCombin = REP_OUT.strip("/") + "/"+combinI
		if str(os.path.isdir(pathCombin)) == "False" :
			os.mkdir(pathCombin)
		print "\tLE PATH A ETE CREE : " + pathCombin
		logging.info("\tLE PATH A ETE CREE : " + pathCombin)

		print "\tTRAITEMENT DES FICHIERS DE LA COMBINAISON"
		logging.info("\tTRAITEMENT DES FICHIERS DE LA COMBINAISON")
		#list fichier a traiter pour chaque combine
		listFilesINC = trait_one_combination_file(combinI,REP_IN,REP_OUT)
		#traitement de la liste des fichiers
		combin_all_file(REP_IN,REP_OUT,pathCombin,DATA_TABLE_FILE_NAME,listFilesINC,DATA_MATRICE_VENN)
		

		print "FIN ____________________ TRAITEMENT DE LA COMBINAISON "+combinI+"___________________________________________"
		logging.info("FIN _____________ TRAITEMENT DE LA COMBINAISON  "+combinI+"_________________________________")




#RECUPERATION LISTE ID DANS CHAQUE FICHIER 
def create_list_from_cln_all_file(fileName,numCln):
	lenClnX=0
	listClnX=[]
	
	fin= open(fileName,"r")
	lines = fin.readlines()
	
	for line in lines:
		 if line != lines[0] :		# SUPPRESSION DES ENTETES DES CLN
		 	 lineIN = str(line.strip("\r\n"))
			 lineIN = lineIN.split("\t")
			 listClnX.append(lineIN[numCln])
	listClnX = sorted(set(listClnX))
	fin.close() 
	print "\t NOMBRE D'IDS TOTAL SANS DOUBLONS : " + str(len(listClnX)) + " DANS LE FICHIER : " + fileName
	logging.info("\t NOMBRE D'IDS TOTAL SANS DOUBLONS : " + str(len(listClnX)) + " DANS LE FICHIER : " + fileName)
	return listClnX

#RECUPERATION LISTE ID DANS CHAQUE FICHIER 
def create_id_list_cln_wO_msg(fileName,numCln):
	lenClnX=0
	listClnX=[]
	
	fin= open(fileName,"r")
	lines = fin.readlines()
	
	for line in lines:
		 if line != lines[0] :		# SUPPRESSION DES ENTETES DES CLN
		 	 lineIN = str(line.strip("\r\n"))
			 lineIN = lineIN.split("\t")
			 listClnX.append(lineIN[numCln])
	listClnX = sorted(set(listClnX))
	fin.close() 
	return listClnX

#CREATION DATA_TABLE POUR R 
def dataTableFile_creat(REP_IN,REPORT_DIR_NAME,REP_OUT,DATA_TABLE_FILE_NAME,listFilesIn):
	recupFileNameHeader =""
	recupFilLN = ""
	listID_sansdb =[]
	lineList =[]
	listFileInRep = listFilesIn
	print "\tETAPE DE CONSTRUCTION DU DATA TABLE POUR LA CONSTRUCTION DU VENN "
	logging.info("\tETAPE DE CONSTRUCTION DU DATA TABLE POUR LA CONSTRUCTION DU VENN ")

	#Recuperation des ids de tous les fichies SANS DOUBLONS
	for namefile in listFileInRep:
		#Recuperation de la liste d'id trier- sans doublons d un fichiers / cln correspondant au id , num 3
		listID_sansdb = listID_sansdb + (create_list_from_cln_all_file(REP_IN.strip("/")+"/"+namefile,4))
	listID_sansdb = sorted(set(listID_sansdb))

	print "\t NOMBRE D'IDS TOTAL SANS DOUBLONS POUR TOUS LES FICHIERS : " + str(len(listID_sansdb)) 
	logging.info("\t NOMBRE D'IDS TOTAL SANS DOUBLONS POUR TOUS LES FICHIERS : " + str(len(listID_sansdb)) )
	
	#for namefile in listFileInRep:
	#Ouverture du fichier en lecture
	datatable_file = open(REPORT_DIR_NAME + "/" +DATA_TABLE_FILE_NAME,"w")

	#print "Ids/Fnames\t" + recupFileNameHeader
	#datatable_file.write("Ids\t\n")	

	for idsT in listID_sansdb:
		#print idsT + "\n"	
		datatable_file.write(idsT + "\t\n")
	#Fermeture du fichier

	datatable_file.close()

	print "LECTURE FICHIER CONTENANT LES ID SANS DOUBLONS ..."
	logging.info("LECTURE FICHIER CONTENANT LES ID SANS DOUBLONS ...")
	#Ouverture du fichier en lecture
	datatable_fileI = open(REPORT_DIR_NAME + "/" +DATA_TABLE_FILE_NAME,"r")
	lines = datatable_fileI.readlines()
	
	
	for line in lines:
		lineList.append(line.strip("\t\r\n"))
		#print lineList
		
	for namefile in listFileInRep:
		listI= create_id_list_cln_wO_msg(REP_IN.strip("/")+"/"+namefile,4)
	
		print "\t___DEBUT DE GENERATION DU FICHIERS 0/1 POUR " + namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt")
		logging.info("\t___DEBUT DE GENERATION DU FICHIERS 0/1 POUR " + namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt"))
		#Ouverture du fichier en ecriture
		finDF= open(REPORT_DIR_NAME+"/"+"dataTableVenn_"+namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt")+".txt","w")
		finDF.write (namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt")+"\n")
	

		for idall in lineList:
			if idall in listI :
				finDF.write(str(1) + "\n")
			else:
				finDF.write(str(0) + "\n")

		finDF.close()
		print "\t___FIN DE GENERATION DU FICHIERS 0/1 POUR " + namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt")
		logging.info("\t___FIN DE GENERATION DU FICHIERS 0/1 POUR " + namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt"))
		recupFileNameHeader = recupFileNameHeader + " " +REPORT_DIR_NAME+"/"+"dataTableVenn_"+namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt")+".txt"
	datatable_fileI.close()
	
	#Creation matrice 
	#ajout IDS dans le fichier contenant tous les ids :
	fileAllID = open (REPORT_DIR_NAME + "/" +DATA_TABLE_FILE_NAME,"w")
	fileAllID.write("IDS_ALL_SANS_DOUBLONS\n")
	for idsT in listID_sansdb:
		fileAllID.write(idsT + "\n")
	fileAllID.close()

	print "\t___DEBUT CREATION MATRICE POUR LE DIAGRAMME DE VENN "
	logging.info("\t___DEBUT CREATION MATRICE POUR LE DIAGRAMME DE VENN ")
	cmd= "paste " + REPORT_DIR_NAME + "/" +DATA_TABLE_FILE_NAME + " " + recupFileNameHeader +" > "+ REP_OUT + "/"+"data_Table_For_Venn.txt"	
	os.system(cmd)

	cmd2= "paste " + recupFileNameHeader +" > "+ REP_OUT + "/"+"matrix.txt"	
	os.system(cmd2)

	print "\t___FIN CREATION MATRICE POUR LE DIAGRAMME DE VENN "
	logging.info("\t___FIN CREATION MATRICE POUR LE DIAGRAMME DE VENN ")
	
	#nettoyage des fichiers intermédiaires 
	for namefile in listFileInRep:
		os.system("rm " + REPORT_DIR_NAME+"/"+"dataTableVenn_"+namefile.strip("_snpeff_snpsift_OneLineEff_DF.txt")+".txt")
	print "FIN DE LA LECTURE DU FICHIER CONTENANT LES ID SANS DOUBLONS."
	logging.info("FIN DE LA LECTURE DU FICHIER CONTENANT LES ID SANS DOUBLONS.")

	
#COMBI DE TOUS LES FICHIERS 
def combin_all_file(REP_IN,REPORT_DIR_NAME,REP_OUT,DATA_TABLE_FILE_NAME,listFilesIn,DATA_MATRICE_VENN):

	#__CREATION DU FICHIER DATA_TABLE POUR R
	#Lister les fichiers du repertoire d entree
	listFileInRep = listFilesIn

	print "\tFILES TO TREAT : " + str(listFileInRep)
	logging.info("FILES TO TREAT : " + str(listFileInRep))
	
	print "\tNOMBRE DE FICHIER A TRAITER : " + str(len(listFileInRep))
	logging.info("\tNOMBRE DE FICHIER A TRAITER : " + str(len(listFileInRep)))
	
	#__ETAPE DE CONSTRUCTION DU DATA TABLE POUR LA CONSTRUCTION DU VENN 
	dataTableFile_creat(REP_IN,REPORT_DIR_NAME,REP_OUT,DATA_TABLE_FILE_NAME,listFilesIn)

	
	print "CREATION DU REPERTOIRES CORRESPONDANT A LA COMBINAISON DE TOUT LES FICHIERS " + REP_OUT
	logging.info( "\tCREATION DU REPERTOIRES CORRESPONDANT A LA COMBINAISON DE TOUT LES FICHIERS" + REP_OUT)

	print "\t__DEBUT LECTURE DE LA MATRICE ET GENERATION DU FICHIER DES IDS COMMUNS / UNIQS "
	logging.info("\t__DEBUT LECTURE DE LA MATRICE ET GENERATION DU FICHIER DES IDS COMMUNS / UNIQS ")
	#ouvrir le fichier contenant les IDs communs :
	commFile= open (REP_OUT+"/Id_comm.txt","w")
	commFile.write("IDS_COMMUNS\n")

	#ouvrir le fichier contenant les IDs uniqs :
	uniqFileIds= open (REP_OUT+"/Id_uniq.txt","w")
	uniqFileIds.write("IDS_UNIQS\n")
	#lecture de la matrice 
	matriceIn = open(REP_OUT+"/"+DATA_MATRICE_VENN,"r")
	lines = matriceIn.readlines()
	
	listUniqID=[]
	listCommID=[]
	
	commNbr=0
	uniqNbr=0
	comm2AtLeast=0
	idTraitNbr=0
	for line in lines:
		if line != lines[0] :
			line=line.strip("\r\n")
			listLineFileds = line.split("\t")
			#print listLineFileds
			#print listLineFileds.count(str(1))
			if listLineFileds.count(str(1)) == len(listFileInRep):
				#print str(listLineFileds.count(str(1))) +"/" +str(len(listFileInRep))
				#print listLineFileds[0]
				commFile.write(listLineFileds[0]+"\n")
				commNbr = commNbr + 1
				listCommID.append(listLineFileds[0])
			elif listLineFileds.count(str(1)) == 1:
				#print listLineFileds[0]
				uniqFileIds.write(listLineFileds[0]+"\n")
				uniqNbr = uniqNbr + 1
				listUniqID.append(listLineFileds[0])
			else:
				comm2AtLeast = comm2AtLeast +1
			idTraitNbr= idTraitNbr +1
		
	print "\tNOMBRE D'IDS TRAITES : " + str(idTraitNbr)	
	logging.info("\tNOMBRE D'IDS TRAITES : " + str(idTraitNbr))		
	print "\tNOMBRE D'IDS COMMUNS A TOUS LES FICHIERS : " + str(commNbr)
	logging.info("\tNOMBRE D'IDS COMMUNS A TOUS LES FICHIERS : " + str(commNbr))	
	print "\tNOMBRE D'IDS COMMUNS A AUX MOINS DEUX FICHIERS (Si nbrFichier > 2, sinon =0): " + str(comm2AtLeast)
	logging.info("\tNOMBRE D'IDS COMMUNS A AUX MOINS DEUX FICHIERS (Si nbrFichier > 2, sinon =0): " + str(comm2AtLeast))
	print "\tNOMBRE D'ID UNIQUE A UN SEUL FICHIER : " + str(uniqNbr)
	logging.info("\tNOMBRE D'ID UNIQUE A UN SEUL FICHIER : " + str(uniqNbr))
	
	#Fermeture fichiers
	matriceIn.close()
	commFile.close()
	uniqFileIds.close()

	print "\t__FIN LECTURE DE LA MATRICE ET GENERATION DU FICHIER DES IDS COMMUNS / UNIQS "
	logging.info("\t__FIN LECTURE DE LA MATRICE ET GENERATION DU FICHIER DES IDS COMMUNS / UNIQS ")
	
	
	#print listUniqID
	print "DEBUT ___ GENERATION DES FICHIERS DES UNIQUES PAR FICHIERS "
	#ouverture des fichiers et verification des uniques
	nbrUniqIdInFile = []
	for namefile in listFileInRep:
		pathFileName = REP_IN.strip("/")+"/"+namefile
		#print pathFileName
		
		#Fichier d entree
		finList = open(pathFileName,"r")
		linesFin = finList.readlines()
		
		#Fichier de sortie
		pathFileOUt= REP_OUT.strip("/") + "/"+namefile.strip(".txt") + "_UNIQ.txt"
		foutList = open(pathFileOUt,"w")
		foutList.write("CHROMOSOME\tPOSITION\tREFERENCE\tCHANGE\tCUSTOM_SNP\tCUSTOM_VARIATION\tCHANGE_TYPE\tDP4_REF_FWD\tDP4_REF_REV\tDP4_ALT_FWD\tDP4_ALT_REV\tDP4_TOTAL_REF\tDP4_TOTAL_ALT\tCOVERAGE\tHOM_HET\tQUALITY\tID_GENE\tEFFECT\tNBR_BASE\tOLD_AA/NEW_AA\tOLD_CODON/NEW_CODON\tCODON_NUM(CDS)\tCODON_DEGENERACY\n")
		for linef in linesFin :
			if linef != linesFin[0] :
				linef = linef.strip("\r\n")
				lineListField = linef.split("\t")
				#print lineListField[4]
				if lineListField[4] in listUniqID:
					foutList.write(linef+"\n")
					nbrUniqIdInFile.append(lineListField[4])
		print "\tNOMBRE D ID UNIQUE DANS LE FICHIER : " + namefile.strip(".txt") + "_UNIQ.txt est " + str(len(sorted(set(nbrUniqIdInFile))))
		logging.info("\tNOMBRE D ID UNIQUE DANS LE FICHIER : " + namefile.strip(".txt") + "_UNIQ.txt est " + str(len(sorted(set(nbrUniqIdInFile)))))
		finList.close()
		foutList.close()
		nbrUniqIdInFile = []
	print "FIN ___ GENERATION DES FICHIERS DES UNIQUES PAR FICHIERS "
	logging.info("FIN ___ GENERATION DES FICHIERS DES UNIQUES PAR FICHIERS ")

	print "DEBUT ___ GENERATION DU  FICHIER DES COMMUNS A TOUS LES FICHIERS "
	logging.info("DEBUT ___ GENERATION DU  FICHIER DES COMMUNS A TOUS LES FICHIERS ")

	#ouvrir le fichier contenant les lignes correspondant aux ids communs
	pathout0=REP_OUT.strip("/") + "/"+"/CommAllFiles.txt"
	commFilewithL= open (pathout0,"w")
	commFilewithL.write("CHROMOSOME\tPOSITION\tREFERENCE\tCHANGE\tCUSTOM_SNP\tCUSTOM_VARIATION\tCHANGE_TYPE\tDP4_REF_FWD\tDP4_REF_REV\tDP4_ALT_FWD\tDP4_ALT_REV\tDP4_TOTAL_REF\tDP4_TOTAL_ALT\tCOVERAGE\tHOM_HET\tQUALITY\tID_GENE\tEFFECT\tNBR_BASE\tOLD_AA/NEW_AA\tOLD_CODON/NEW_CODON\tCODON_NUM(CDS)\tCODON_DEGENERACY\n")

	#Fichier d entree
	pathFileName0 = REP_IN.strip("/")+"/"+listFileInRep[0]
	finList0 = open(pathFileName0,"r")
	linesFin0 = finList0.readlines()
	for linef in linesFin0 :
		if linef != linesFin0[0] :
			linef = linef.strip("\r\n")
			lineListField = linef.split("\t")
			if lineListField[4] in listCommID:
				commFilewithL.write(linef+"\n")
	commFilewithL.close()
	finList0.close()
	print "FIN ___ GENERATION DU  FICHIER DES COMMUNS A TOUS LES FICHIERS "
	logging.info("FIN ___ GENERATION DU  FICHIER DES COMMUNS A TOUS LES FICHIERS ")
	
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- TRAITEMENT -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#-- FIN

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------- MAIN -------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#
# ___ MAIN 
def main(argv):
	#__LogFile
	LOG_FILE_NAME = "./LogFile.log"
	log_report(LOG_FILE_NAME)

	DATA_TABLE_FILE_NAME = "Id_all.txt"
	DATA_MATRICE_VENN ="data_Table_For_Venn.txt"

	#___ TEST DE VERIFICATION DU NOMBRE DES ARGUMENTS  ET TRAITEMENT CORRESPONDANT----
	verif_lastArg(argv,LOG_FILE_NAME,DATA_TABLE_FILE_NAME,DATA_MATRICE_VENN)


if __name__ == "__main__":
	main(sys.argv[1:])



