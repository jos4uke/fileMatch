#__author__ = "BEN HASSINE Najla(Najla.Ben-Hassine@versailles.inra.fr)" #/
#__version__ = "1.1"							#/
#__date__ = "AOUT 2013"							#/
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
" usage : fileMatch <DIR_IN> <DIR_OUT> <F1> <F2> ... <Fn> <-A/-C/-Cn/-AC/-ACn>"
" -h    : vous avez besoin de 2 fichiers .txt (au moins), pour faire le traitement."
	" ** l'outil peut etre lancer de deux façons: "
"	1/ En specifiant une liste de fichiers."
"	2/ Sans specifier une liste de fichiers."

" ** La commande pour lancer l'outil en specifiant une liste de fichier : "
"	cheminExecutable <Repertoire_dentree> <Repertoire_de_sortie> <file1.txt> <file2.txt>  -<Type_de_traitment> "

" ** La commande pour lancer l'outil SANS SPECIFIE une liste de fichier : Tous les fichiers .txt du repertoire seront traites."
"	cheminExecutable <Repertoire_dentree> <Repertoire_de_sortie>  -<Type_de_traitment> "

" ** Trois types de traitements existent : "
" -A : Traitement de l'ensemble de fichier. Un seul dossier sera cree en sortie : AllFilesCombin "
" -C : Traitement des combinaisons de fichiers. Seuls les dossiers correspondant aux combinaisons seront crees. "
" -AC: C'est la combinaison des deux traitements precedents. Deux types de dossiers seront crees. Un dossier AllFilesCombin et les dossiers correspondant aux combinaisons. "
" n: C'est le type de combinaison souhaitee : 2 pour 2a2, 3 pour 3a3, 4 pour 4a4, 5 pour 5a5."
" NB: chaque dossier cree contient un fichier contenant les communs entre les fichiers, et un fichier pour chaque fichier traite, correspondant aux uniques de celui-ci."

" ** Recommandations: "
"	- Copier les donnees a traiter dans un nouveau repertoire qui sera le repertoire d'entree. "
"	- Verifier la liste des fichiers contenu dans le repertoire d'entree (Des sorties .txt du pipeline mutdetect du type nomEchantillon_snpeff_snpsift_OneLineEff_DF.txt)"
"	- Creation d'un repertoire de sortie en dehors du repertoire d'entree."
"	- Verifier votre repertoire de sortie a chaque fois que vous lancer l'outil, pour ne pas ecraser des anciennes analyses."
"	- Les fichiers passes en argument doivent imperativement appartenir au repertoire d'entree."


" ** Remarques : "
"Le developpeur de logiciel ne prend pas la responsabilite de l'integrite de vos donnees:"
"-  Si votre serveur Linux en production a d'une façon ou d'une autre perdu toute raison et a du meme coup detruit vos precieuses donnees (aucun de ces aleas n'a ete enregistre, naturellement, mais nous evoquons une hypothetique eventualite) "
"- Si mauvaises manipulation entrainent la perte de vos donnees."
