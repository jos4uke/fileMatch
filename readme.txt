uthor__ = "BEN HASSINE Najla(Najla.Ben-Hassine@versailles.inra.fr)" #/
#__version__ = "1.0"				         		#/
#__copyright__ = "Copyright (c) 2013-2014 BHN"                         	#/
#__license__ = "GROUPE DEV IJPB"			                #/
#/////////////////////////////////////////////////////////////////////////

"""
VERSION PYTHON UTILISEE:  Python 2.7.3 (64-bit)

PROGRAMME : MERGE DE N FICHIER .TXT (FICHIERS DE REVE POUR SNPEFF VERSION (snpEff_dev))

MODULE : TRAITEMENT DE N FICHIER .txt SORTIE DE SNP_EFF_DEV FORMATE PAR (dreamFileMaker) 
"""

"**************"
" AIDE :"
"**************"
" usage : ./fileMatch <DIR_IN> <DIR_OUT> <F1> <F2> ... <Fn> <-A/-C/-AC>"
" -h    : vous avez besoin de 2 fichiers .txt (au moins), pour faire le traitement."

" ** l'outil peut être lancer de deux façons: "
"	1/ En spécifiant une liste de fichiers."
"	2/ Sans spécifier une liste de fichiers."

" ** La commande pour lancer l'outil en spécifiant une liste de fichier : "
"	cheminExecutable <Repertoire_dentree> <Repertoire_de_sortie> <file1.txt> <file2.txt>  -<Type_de_traitment> "

" ** La commande pour lancer l'outil SANS SPECIFIE une liste de fichier : Tous les fichiers .txt du répertoire seront traités."
"	cheminExecutable <Repertoire_dentree> <Repertoire_de_sortie>  -<Type_de_traitment> "

" ** Trois types de traitements existent : "
" -A : Traitement de l'ensemble de fichier. Un seul dossier sera créé en sortie : AllFilesCombin "
" -C : Traitement des combinaisons de fichiers. Seuls les dossiers correspondant aux combinaisons de fichier 2 à 2 seront crées /  exp : file1___file2 "
" -AC: C'est la combinaison des deux traitements précédents. Deux types de dossiers seront créés. Un dossier AllFilesCombin et les dossiers correspondant aux combinaisons. "

" ** Recommandations: "
"	- Copier les données à traiter dans un nouveau répertoire qui sera le répertoire d'entrée. "
"	- Vérifier la liste des fichiers contenu dans le répertoire d'entrée (Des sorties .txt du pipeline mutdetect du type nomEchantillon_snpeff_snpsift_OneLineEff_DF.txt)"
"	- Création d'un répertoire de sortie en dehors du répertoire d'entrée."
"	- Vérifier votre répertoire de sortie à chaque fois que vous lancer l'outil, pour ne pas écraser des anciennes analyses."
"	- Les fichiers passés en argument doivent impérativement appartenir au répertoire d'entrée."


" ** Remarques : "
"Le développeur de logiciel ne prend pas la responsabilité de l'intégrité de vos données:"
"-  Si votre serveur Linux en production a d'une façon ou d'une autre perdu toute raison et a du même coup détruit vos précieuses données (aucun de ces aléas n'a été enregistré, naturellement, mais nous évoquons une hypothétique éventualité) "
"- Si mauvaises manipulation entrainent la perte de vos données."

