##import pandas as pd 
##import xml.etree.ElementTree as ET
##
##tree = ET.parse("curriculo.xml")
##root = tree.getroot() 
##
##root=tree.getroot()
##print (root)
##print (root[0][7][0].attrib)
import time
from bs4 import BeautifulSoup
import os
import requests
import re
import zipfile
import numpy as np
import pandas as pd
from .extrafuns import fun_result
from testapp1.models import (
    Trabalho,
    CapitulosDeLivrosPublicados,
    Education,
    OtherProductions,
    Person,
    ProducaoTecnica,
    Project,
    Publications,
)
import mysql.connector
mydatabase=mysql.connector.connect(host='sql10.freemysqlhosting.net',port=3306,user='sql10639123',passwd='VyKJuJnrrl',db='sql10639123',charset='utf8',use_unicode=True)


def compare(fullername):
    maincursor=mydatabase.cursor()
    boleanvalue=False



    maincursor.execute('''SELECT full_name
                            FROM testapp1_person
                        ''')
    for row in maincursor:
        test=(row[0])
        print (test)
        print(fullername)

        if test==fullername:
            boleanvalue=True 
    maincursor.close() 

    return boleanvalue

def update_person_with_django_by_fullname(fullname, new_last_name,new_cite, new_city, new_state, new_description, new_workplace, new_update, new_orcid):
    try:
        person = Person.objects.get(Full_name=fullname)
        person.Last_Name = new_last_name
        person.Citation=new_cite
        person.City = new_city
        person.State = new_state
        person.Description = new_description
        person.Workplace = new_workplace
        person.Update = new_update
        person.ORCID = new_orcid
        person.save()
        print(f"Person with Fullname '{fullname}' updated with Django ORM.")
    except Person.DoesNotExist:
        print(f"Person with Fullname '{fullname}' does not exist.")
def main(zipname):


    with zipfile.ZipFile(zipname, 'r') as main_zip:
        main_folder_name = os.path.splitext(os.path.basename(zipname))[0]  # Get the name of the main zip file without the extension
        main_folder_path = os.path.join('temp', main_folder_name)  # Extract to a temporary directory

        main_zip.extractall(main_folder_path)

        for root, dirs, files in os.walk(main_folder_path):
            for filename in files:
                if filename.endswith('.zip'):
                    inner_zip_path = os.path.join(root, filename)

                    with zipfile.ZipFile(inner_zip_path, 'r') as inner_zip:
                        df_papers_bool=False
                        df_fullname_bool=False
                        df_advis_bool=False
                        df_capit_bool=False
                        df_ccd_bool=False
                        df_ppe_bool=False
                        df_ens_bool=False
                        df_trabalho_bool=False
                        lattesxmldata = inner_zip.open('curriculo.xml')
                        soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')
                        cv = soup.find_all('curriculo-vitae')
                        
                        if len(cv) == 0:
                            print('curriculo vitae nao encontrado para', zipname)
                        else:
                            # listas para armazenamento de dados producao tecnica
                            for i in range(len(cv)):
                                dg = cv[i].find_all('dados-gerais')
                                # VERIFICANDO se ha dados gerais
                                if len(dg) == 0:
                                    print('Dados gerais nao encontrados para', zipname)
                                else:
                                    for j in range(len(dg)):
                                        # definindo nome completo
                                        gendata = str(dg[j])
                                        result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                                        gendata)
                                        cc = fun_result(result)
                                        fullname = cc
                                        df_thename_bool=True
                                        print (fullname)














                        livscaps = soup.find_all('livros-e-capitulos')
                        # VERIFICANDO se ha livros e capitulos
                        if len(livscaps) == 0:
                            print('Capitulos publicados nao encontrados para')
                        else:
                            capspuborg = livscaps[0].find_all('capitulos-de-livros-publicados')
                            # VERIFICANDO se ha capitulos
                            if len(capspuborg) == 0:
                                print('Capitulos publicados nao encontrados para', zipname)
                            else:
                                cappuborg = capspuborg[0].find_all('capitulo-de-livro-publicado')
                                # listas para armazenamento de dados livros e capitulos
                                ls_cap_title = []
                                ls_cap_year = []
                                ls_cap_lang = []
                                ls_cap_edit = []
                                ls_cap_authors = []
                                ls_cap_authororder = []
                                ls_cap_orders = []
                                # a partir de cada livro capitulo publicado extrair inf de interesse
                                for i in range(len(cappuborg)):
                                    # dados basicos do livro
                                    dbc = cappuborg[i].find_all('dados-basicos-do-capitulo')
                                    capitdb = str(dbc)
                                    # definindo o nome do capitulo
                                    result = re.search(
                                        'titulo-do-capitulo-do-livro=\"(.*)\" titulo-do-capi',
                                        capitdb)
                                    cc = fun_result(result)
                                    ls_cap_title.append(cc)
                                    # print(cc)
                                    # definindo ano do livro
                                    result = re.search('ano=\"(.*)\" doi',
                                                    capitdb)
                                    cc = fun_result(result)
                                    ls_cap_year.append(cc)
                                    # print(cc)
                                    # definindo idioma do livro
                                    result = re.search('idioma=\"(.*)\" meio-de-divulgacao=',
                                                    capitdb)
                                    cc = fun_result(result)
                                    ls_cap_lang.append(cc)
                                    # detalhamento do livro
                                    ddc = cappuborg[i].find_all('detalhamento-do-capitulo')
                                    capitdt = str(ddc)
                                    # definindo editora
                                    result = re.search(
                                        'nome-da-editora=\"(.*)\" numero-da-edicao-r',
                                        capitdt)
                                    cc = fun_result(result)
                                    ls_cap_edit.append(cc)
                                    # print(cc)
                                    # autores do livro
                                    aut = cappuborg[i].find_all('autores')
                                    ls_allauthors = []
                                    ls_allauthororder = []
                                    ls_allorders = []
                                    ls_authororder = []
                                    for j in range(len(aut)):
                                        auth = str(aut[j])
                                        result = re.search(
                                            'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                                            auth)
                                        if result is None:
                                            cc = 'VAZIO'
                                        else:
                                            cc = result.group(1)
                                            nca = result.group(1)  # nomecompletoautora
                                        ls_allauthors.append(cc)
                                        # print(cc)
                                        # order de autoria
                                        result = re.search(
                                            'ordem-de-autoria=\"(.*)\"',
                                            auth)
                                        if result is None:
                                            cc = 'VAZIO'
                                        else:
                                            cc = result.group(1)
                                            ncao = result.group(1)
                                        ls_allauthororder.append(cc)
                                        if fullname == nca:
                                            ls_authororder.append(ncao)
                                            # print(fullname + ' ' + ncao)
                                        # print(cc)
                                    ls_cap_authors.append(ls_allauthors)
                                    ls_cap_authororder.append(ls_allauthororder)
                                    ls_cap_orders.append(ls_authororder)
                                    # print(cc)
                                # DataFrame livros publicados
                                df_capit = pd.DataFrame({'TITLE': ls_cap_title,
                                                        'YEAR': ls_cap_year,
                                                        'LANG': ls_cap_lang,
                                                        'EDITORA': ls_cap_edit,
                                                        'AUTHOR': ls_cap_authors,
                                                        'ORDER': ls_cap_authororder,
                                                        'ORDER_OK': ls_cap_orders})
                                
                                df_capit_bool=True

                        ##CREATE TABLE Education
                        ##(
                        ##Nome CHAR(20) NOT NULL,
                        ##Year_INI VARCHAR (20) NOT NULL,
                        ##Year_FIN VARCHAR(20),
                        ##Month_INI VARCHAR (20) NOT NULL,
                        ##Month_FIN VARCHAR(20),
                        ##Course VARCHAR(200),
                        ##Type CHAR(50),
                        ##Disc CHAR(20),
                        ##    CONSTRAINT EduPK PRIMARY KEY(Nome,Year_INI,Course),
                        ##CONSTRAINT PersonFK FOREIGN KEY (Stativid,Låsnr) 
                        ##REFERENCES Lås (Stativid,Låsnr);



















                        cv = soup.find_all('curriculo-vitae')
                        # VERIFICANDO se ha demais tipos de producao
                        if len(cv) == 0:
                            print('curriculo vitae nao encontrado para', zipname)
                        else:
                            # listas para armazenamento de dados producao tecnica
                            ls_name_full = []
                            ls_name_last = []
                            ls_name_id = []
                            ls_city = []
                            ls_state = []
                            ls_citado = []
                            ls_orcid = []
                            ls_abstrac = []
                            ls_update = []
                            ls_address_enterp = []
                            for i in range(len(cv)):
                                # definindo atualizacao
                                cvdata = str(cv[i])
                                result = re.search('data-atualizacao=\"(.*)\" hora-atualizacao',
                                                cvdata)
                                if result is None:
                                    cc = 'VAZIO'
                                else:
                                    cc = result.group(1)
                                    upd = str(cc[0:2]) + '-' + \
                                        str(cc[2:4]) + '-' + str(cc[4:])
                                    cc = upd
                                    # print(cc)
                                    ls_update.append(cc)
                                dg = cv[i].find_all('dados-gerais')
                                # VERIFICANDO se ha dados gerais
                                if len(dg) == 0:
                                    print('Dados gerais nao encontrados para', zipname)
                                else:
                                    for j in range(len(dg)):
                                        # definindo nome completo
                                        gendata = str(dg[j])
                                        result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                                        gendata)
                                        cc = fun_result(result)
                                        ls_name_full.append(cc)
                                        lastname = cc.split(' ')[-1]
                                        ls_name_last.append(lastname)
                                        idd = zipname.split('.')[0]
                                        ls_name_id.append(idd)
                                        # definindo cidade
                                        gendata = str(dg[j])
                                        result = re.search(
                                            'cidade-nascimento=\"(.*)\" data-faleci',
                                            gendata)
                                        cc = fun_result(result)
                                        ls_city.append(cc)
                                        # definindo estado
                                        gendata = str(dg[j])
                                        result = re.search('uf-nascimento=\"(.*)\"><res',
                                                        gendata)
                                        cc = fun_result(result)
                                        ls_state.append(cc)
                                        # definindo nome em citacoes
                                        gendata = str(dg[j])
                                        result = re.search(
                                            'nome-em-citacoes-bibliograficas=\"(.*)\" orcid-id',
                                            gendata)
                                        cc = fun_result(result)
                                        ls_citado.append(cc)
                                        # definindo ORCID
                                        gendata = str(dg[j])
                                        result = re.search('orcid-id=\"(.*)\" pais-de-nacionali',
                                                        gendata)
                                        cc = fun_result(result)
                                        ls_orcid.append(cc)

                                rescv = cv[i].find_all('resumo-cv')
                                address = cv[i].find_all('endereco')
                                # VERIFICANDO se ha resumo
                                if len(rescv) == 0:
                                    print('Resumo cv nao encontrados para', zipname)
                                    cc = 'VAZIO'
                                    ls_abstrac.append(cc)
                                else:
                                    for j in range(len(rescv)):
                                        # definindo resumo
                                        abstdata = str(rescv[j])
                                        result = re.search('texto-resumo-cv-rh=\"(.*)\" texto-resumo-cv-rh-en=',
                                                        abstdata, re.DOTALL)
                                        if result is None:
                                            cc = 'Nao foi possivel extrair o resumo'
                                        else:
                                            cc = result.group(1)
                                        ls_abstrac.append(cc)
                                # VERIFICANDO se ha endereco
                                if len(address) == 0:
                                    print('Endereco nao encontrado para', zipname)
                                    cc = 'VAZIO'
                                    ls_address_enterp.append(cc)
                                else:
                                    for j in range(len(address)):
                                        # verificando se ha endereco profissional
                                        address_prof = address[j].find_all('endereco-profissional')
                                        if len(address_prof) == 0:
                                            print('Endereco profissional nao encontrado para', zipname)
                                            cc == 'VAZIO'
                                            ls_address_enterp.append(cc)
                                        else:
                                            # definindo endereco
                                            addressdata = str(address_prof[0])
                                            result = re.search('nome-instituicao-empresa=\"(.*)\" nome-orgao=',
                                                            addressdata, re.DOTALL)
                                            if result is None:
                                                cc = 'Nao foi possivel extrair o endereco profissional'
                                            else:
                                                cc = result.group(1)
                                                ls_address_enterp.append(cc)
                            # DataFrame nome completo e sobrenome
                            df_fullname = pd.DataFrame({'ID': ls_name_id,
                                                        'FULL_NAME': ls_name_full,
                                                        'LAST_NAME': ls_name_last,
                                                        'CITADO': ls_citado,
                                                        'CITY': ls_city,
                                                        'STATE': ls_state,
                                                        'RESUME': ls_abstrac,
                                                        'UPDATE': ls_update,
                                                        'ADDRESS_ENTERP': ls_address_enterp,
                                                        'ORCID': ls_orcid})
                            df_fullname_bool=True

                        print (df_fullname['ORCID'])

































                        # lendo do zipfile
                        # zipname = '3275865819287843.zip'
                        # zipname = '8190371175828378.zip'
                        # zipname = '5859946324646438.zip'

                        # ttfile = open('tt.xml', 'w')
                        # ttfile.write(soup.prettify())
                        # ttfile.close()
                        # extrair todas as atividades profissionais
                        ap = soup.find_all('atuacao-profissional')
                        # VERIFICANDO se ha atuacao profissional
                        if len(ap) == 0:
                            print('Atuacao profissional nao encontrada para', zipname)
                        else:
                            # listas para armazenamento de dados PROJETOS PESQ e EXT
                            ls_inst = []
                            ls_yini = []
                            ls_yfin = []
                            ls_mini = []
                            ls_mfin = []
                            ls_curs = []
                            ls_tipo = []
                            ls_disc = []
                            for i in range(len(ap)):
                                instit = re.search('nome-instituicao=\"(.*)\" sequencia-atividade',
                                                str(ap[i]))
                                instit = fun_result(instit)
                                app = ap[i].find_all('atividades-de-ensino')
                                # a partir das atividades de participacao em projeto, filtra-se todos os
                                # projeto de pesquisa que contem os projetos de ext e pesq que ocorreu
                                # na instituicao
                                # VERIFICANDO se ha participacao em projeto
                                if len(app) == 0:
                                    print(
                                        'Atividades de ensino não encontrada para ', zipname)
                                else:
                                    for j in range(len(app)):
                                        ens = app[j].find_all('ensino')
                                        if len(ens) == 0:
                                            print(
                                                'ensino não encontrado para ', zipname)
                                        else:
                                            for k in range(len(ens)):
                                                # registrando instituicao
                                                ls_inst.append(instit)
                                                # definindo o ano ini
                                                aten = str(ens[k])
                                                result = re.search('ano-inicio=\"(.*)\" codigo-curso',
                                                                aten)
                                                cc = fun_result(result)
                                                ls_yini.append(cc)
                                                # definindo mes inicial
                                                result = re.search('mes-inicio="(.*)" nome-curso=',
                                                                aten)
                                                cc = fun_result(result)
                                                ls_mini.append(cc)
                                                # definindo o ano final
                                                result = re.search('ano-fim="(.*)" ano-inicio',
                                                                aten)
                                                cc = fun_result(result)
                                                
                                                if result is None:
                                                    cc = 'VAZIO'
                                                else:
                                                    cc = result.group(1)
                                                if cc == '':
                                                    cc = 'ATUAL'
                                                ls_yfin.append(cc)
                                                # definindo o mes final
                                                result = re.search('mes-fim="(.*)" mes-inicio',
                                                                aten)
                                                cc = fun_result(result)
                                                
                                                if result is None:
                                                    cc = 'VAZIO'
                                                else:
                                                    cc = result.group(1)
                                                if cc == '':
                                                    cc = 'ATUAL'
                                                ls_mfin.append(cc)
                                                # definindo o curso
                                                result = re.search(
                                                    'nome-curso=\"(.*)\" nome-curso-i',
                                                    aten)
                                                cc = fun_result(result)
                                                ls_curs.append(cc)
                                                # definindo o tipo
                                                result = re.search('tipo-ensino=\"(.*)\"\>\<',
                                                                aten)
                                                cc = fun_result(result)
                                                ls_tipo.append(cc)
                                                # definindo disciplinas
                                                ensdisc = ens[k].find_all('disciplina')
                                                if len(ensdisc) == 0:
                                                    print('nao ha discip nesta ativ ensino ', zipname)
                                                else:
                                                    ls_dis = []
                                                    for kk in range(len(ensdisc)):
                                                        dis = str(ensdisc[kk])
                                                        result = re.search(
                                                            '=\"\d\"\>(.*)\<\/disciplina', dis)
                                                        cc = fun_result(result)
                                                        ls_dis.append(cc)
                                                ls_disc.append(ls_dis)
                                                # ------------------------------------------------------------
                            # DataFrame para os dados
                            df_ens = pd.DataFrame({'INSTITUTION': ls_inst,
                                                'YEAR_INI':  ls_yini,
                                                'YEAR_FIN':  ls_yfin,
                                                'MONTH_INI': ls_mini,
                                                'MONTH_FIN': ls_mfin,
                                                'COURSE':    ls_curs,
                                                'TYPE':      ls_tipo,
                                                'DISC': ls_disc
                                                })
                            df_ens.sort_values(['YEAR_INI'], axis=0, inplace=True)

                            df_ens_bool=True



                        print (df_ens['TYPE'])


















                        ap = soup.find_all('atuacao-profissional')
                        # VERIFICANDO se ha atuacao profissional
                        if len(ap) == 0:
                            print('Atuacao profissional nao encontrada para', zipname)
                        else:
                            # listas para armazenamento de dados PROJETOS PESQ e EXT
                            ls_coord_sn = []
                            ls_intproj = []
                            ls_natu = []
                            ls_proj = []
                            ls_yfin = []
                            ls_yini = []
                            # A partir das atividades profissionais, para cada uma delas (Unioeste,
                            # DGF, etc) há diversas atividades, contudo queremos a participação em
                            # projetos. No caso pegamos o ap é 5 que é da unemat.
                            for i in range(len(ap)):
                                app = ap[i].find_all('atividades-de-participacao-em-projeto')
                                # a partir das atividades de participacao em projeto, filtra-se todos os
                                # projeto de pesquisa que contem os projetos de ext e pesq que ocorreu
                                # na instituicao
                                # VERIFICANDO se ha participacao em projeto
                                if len(app) == 0:
                                    print(
                                        'Participacao em projeto em uma das atividades profissionais nao encontrada para', zipname)
                                else:
                                    for j in range(len(app)):
                                        ppe = app[j].find_all('projeto-de-pesquisa')
                                        # definindo o nome do projeto
                                        for k in range(len(ppe)):
                                            proj = str(ppe[k])
                                            result = re.search('nome-do-projeto=\"(.*)\" nome-do-projeto-i',
                                                            proj)
                                            cc = fun_result(result)
                                            ls_proj.append(cc)
                                            # print(cc)
                                            # definindo o ano inicial
                                            # result = re.search('ano-inicio=\"(.*)\" data-certificacao', proj)
                                            result = re.search('ano-inicio="(.*)" data-certificacao',
                                                            proj)
                                            cc = fun_result(result)
                                            ls_yini.append(cc)
                                            # definindo o ano final
                                            result = re.search('ano-fim="(.*)" ano-inicio',
                                                            proj)
                                            cc = fun_result(result)
                                            if result is None:
                                                cc = 'VAZIO'
                                            else:
                                                cc = result.group(1)
                                            if cc == '':
                                                cc = 'ATUAL'
                                            ls_yfin.append(cc)
                                            # definindo a natureza
                                            result = re.search(
                                                'natureza=\"(.*)\" nome-coordenador', proj)
                                            cc = fun_result(result)
                                            ls_natu.append(cc)
                                            # Integrante do projeto
                                            ep = ppe[k].find_all('equipe-do-projeto')
                                            for m in range(len(ep)):
                                                ip = ep[m].find_all('integrantes-do-projeto')
                                                ls_allintproj = []
                                                ls_allcoordsn = []
                                                for m in range(len(ip)):
                                                    integ = str(ip[m])
                                                    result = re.search(
                                                        'nome-completo=\"(.*)\" nome-para-citacao',
                                                        integ)
                                                    cc = fun_result(result)
                                                    ls_allintproj.append(cc)
                                            # definindo se é coordenador SIM ou NAO
                                                    result = re.search(
                                                        'responsavel=\"(.*)\" nome-completo', integ)
                                                    cc = fun_result(result)
                                                    ls_allcoordsn.append(cc)
                                                    # print(ls_allintproj)
                                                    # print(ls_allcoordsn)
                                            ls_intproj.append(ls_allintproj)
                                            ls_coord_sn.append(ls_allcoordsn)
                            # DataFrame para os dados
                            df_ppe = pd.DataFrame({'PROJ': ls_proj,
                                                'YEAR_INI': ls_yini,
                                                'YEAR_FIN': ls_yfin,
                                                'NATUREZA': ls_natu,
                                                'INTEGRANTES': ls_intproj,
                                                'COORDENA': ls_coord_sn})
                            df_ppe_bool=True
















































                        op = soup.find_all('outra-producao')
                        # VERIFICANDO se ha outra producao
                        if len(op) == 0:
                            print('Outras producoes nao encontradas para', zipname)
                        else:
                            # extrair orientacoes concluidas Mestrado e Doutorado*
                            orienconc = op[0].find_all('orientacoes-concluidas')
                            # VERIFICANDO se ha orientacoes pos
                            if len(orienconc) == 0:
                                print('Orientacoes nao encontradas para', zipname)
                            else:
                                # listas para armazenamento de dados producao tecnica
                                ls_adv_year = []
                                ls_adv_nat = []
                                ls_adv_inst = []
                                ls_adv_curso = []
                                ls_adv_student = []
                                ls_adv_type = []
                                ls_adv_suppo = []
                                # extrair orientacoes-concluidas-para-mestrado
                                orienconc_mest = orienconc[0].find_all(
                                    'orientacoes-concluidas-para-mestrado')
                                # VERIFICANDO se ha orientacoes mestrado e doutorado
                                if len(orienconc_mest) == 0:
                                    print('Orientacoes concluidas de mestrado nao encontradas para', zipname)
                                else:
                                    for i in range(len(orienconc_mest)):
                                        # definindo o nome do curso
                                        dadobasico = orienconc_mest[i].find_all(
                                            'dados-basicos-de-orientacoes-concluidas-para-mestrado')
                                        dadobasico = str(dadobasico)
                                        # ano da orientacao
                                        result = re.search('ano=\"(.*)\" doi',
                                                        dadobasico)
                                        cc = fun_result(result)
                                        ls_adv_year.append(cc)
                                        # print(cc)
                                        # natureza da orientacao
                                        result = re.search('natureza=\"(.*)\" pais',
                                                        dadobasico)
                                        cc = fun_result(result)
                                        ls_adv_nat.append(cc)
                                        # print(cc)
                                        # detalhes da orientacao ###
                                        detalhe = orienconc_mest[i].find_all(
                                            'detalhamento-de-orientacoes-concluidas-para-mestrado')
                                        detalhe = str(detalhe)
                                        # instituicao da orientacao
                                        result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_inst.append(cc)
                                        # print(cc)
                                        # nome do curso
                                        result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_curso.append(cc)
                                        # print(cc)
                                        # nome orientado
                                        result = re.search('nome-do-orientado=\"(.*)\" nome-orgao',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_student.append(cc)
                                        # print(cc)
                                        # tipo de orientacao
                                        result = re.search('tipo-de-orientacao=\"(.*)\">',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_type.append(cc)
                                        # print(cc)
                                        # Bolsa
                                        result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_suppo.append(cc)
                                        # print(cc)
                                # ------------------------------------------------------------
                                # extrair orientacoes-concluidas-para-doutorado
                                orienconc_dout = orienconc[0].find_all(
                                    'orientacoes-concluidas-para-doutorado')
                                # VERIFICANDO se ha orientacoes  doutorado
                                if len(orienconc_dout) == 0:
                                    print(
                                        'Orientacoes concluidas de doutorado nao encontradas para', zipname)
                                else:
                                    for i in range(len(orienconc_dout)):
                                        # definindo o nome do curso
                                        dadobasico = orienconc_dout[i].find_all(
                                            'dados-basicos-de-orientacoes-concluidas-para-doutorado')
                                        dadobasico = str(dadobasico)
                                        # ano da orientacao
                                        result = re.search('ano=\"(.*)\" doi',
                                                        dadobasico)
                                        cc = fun_result(result)
                                        ls_adv_year.append(cc)
                                        # print(cc)
                                        # natureza da orientacao
                                        result = re.search('natureza=\"(.*)\" pais',
                                                        dadobasico)
                                        cc = fun_result(result)
                                        ls_adv_nat.append(cc)
                                        # print(cc)
                                        # detalhes da orientacao ###
                                        detalhe = orienconc_dout[i].find_all(
                                            'detalhamento-de-orientacoes-concluidas-para-doutorado')
                                        detalhe = str(detalhe)
                                        # instituicao da orientacao
                                        result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_inst.append(cc)
                                        # print(cc)
                                        # nome do curso
                                        result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_curso.append(cc)
                                        # print(cc)
                                        # nome orientado
                                        result = re.search('nome-do-orientado=\"(.*)\" nome-orgao',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_student.append(cc)
                                        # print(cc)
                                        # tipo de orientacao
                                        result = re.search('tipo-de-orientacao=\"(.*)\">',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_type.append(cc)
                                        # print(cc)
                                        # Bolsa
                                        result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                                                        detalhe)
                                        cc = fun_result(result)
                                        ls_adv_suppo.append(cc)
                                        # print(cc)
                            # ------------------------------------------------------------
                            # outras orientacoes concluidas
                            orienconc_out = op[0].find_all('outras-orientacoes-concluidas')
                            # VERIFICANDO se ha outras orientacoes pos
                            if len(orienconc_out) == 0:
                                print('Outras orientacoes nao encontradas para', zipname)
                            else:
                                for j in range(len(orienconc_out)):
                                    dadobasico = orienconc_out[j].find_all(
                                        'dados-basicos-de-outras-orientacoes-concluidas')
                                    dadobasico = str(dadobasico)
                                    # ano da orientacao
                                    result = re.search('ano=\"(.*)\" doi',
                                                    dadobasico)
                                    cc = fun_result(result)
                                    ls_adv_year.append(cc)
                                    # print(cc)
                                    # natureza da orientacao
                                    result = re.search('natureza=\"(.*)\" pais',
                                                    dadobasico)
                                    cc = fun_result(result)
                                    ls_adv_nat.append(cc)
                                    # print(cc)
                                    # detalhes da orientacao ######
                                    detalhe = orienconc_out[j].find_all(
                                        'detalhamento-de-outras-orientacoes-concluidas')
                                    detalhe = str(detalhe)
                                    # instituicao da orientacao
                                    result = re.search('nome-da-instituicao=\"(.*)\" nome-do-curso=',
                                                    detalhe)
                                    cc = fun_result(result)
                                    ls_adv_inst.append(cc)
                                    # print(cc)
                                    # nome do curso
                                    result = re.search('nome-do-curso=\"(.*)\" nome-do-curso-ingles',
                                                    detalhe)
                                    cc = fun_result(result)
                                    ls_adv_curso.append(cc)
                                    # print(cc)
                                    # nome orientado
                                    result = re.search('nome-do-orientado=\"(.*)\" numero-de-paginas',
                                                    detalhe)
                                    cc = fun_result(result)
                                    ls_adv_student.append(cc)
                                    # print(cc)
                                    # tipo de orientacao
                                    result = re.search('tipo-de-orientacao-concluida=\"(.*)\">',
                                                    detalhe)
                                    cc = fun_result(result)
                                    ls_adv_type.append(cc)
                                    # print(cc)
                                    # Bolsa
                                    result = re.search('flag-bolsa=\"(.*)\" nome-da-agencia',
                                                    detalhe)
                                    cc = fun_result(result)
                                    ls_adv_suppo.append(cc)
                                    # print(cc)
                                # DataFrame orientacoes
                                df_advis = pd.DataFrame({'YEAR': ls_adv_year,
                                                        'NATURE': ls_adv_nat,
                                                        'INSTITUTION': ls_adv_inst,
                                                        'COURSE': ls_adv_curso,
                                                        'STUDENT': ls_adv_student,
                                                        'TYPE': ls_adv_type,
                                                        'SPONSOR': ls_adv_suppo})
                                df_advis_bool=True
                        print()
                        print()
                        print()
                        ##for x,y in df_advis.iterrows():
                        ##    #print (y['YEAR'],y['TYPE'],y['COURSE'],y['NATURE'])
                        ##    
                        ##    var1=y['TYPE']
                        ##    var2=y['YEAR']
                        ##    var3=y['COURSE']
                        ##    var4=y['NATURE']
                        ##    print (var1,var2,var3,var4)









































                        # extrair demais-tipos-de-producao-tecnica
                        dtpt = soup.find_all('demais-tipos-de-producao-tecnica')
                        # VERIFICANDO se ha demais tipos de producao
                        if len(dtpt) == 0:
                            print('Demais tipos de producao nao encontrada para', zipname)
                        else:
                            # listas para armazenamento de dados producao tecnica
                            ls_curscd_name = []
                            ls_curscd_year = []
                            ls_curscd_integ = []
                            # A partir dos demais tipos de producao tecnica extrai-se os cursos,
                            # palestras, etc
                            for i in range(len(dtpt)):
                                ccdm = dtpt[i].find_all('curso-de-curta-duracao-ministrado')
                                # VERIFICANDO se ha cursos
                                if len(ccdm) == 0:
                                    print('Curso de cura duracao nao encontrado para', zipname)
                                else:
                                    for j in range(len(ccdm)):
                                        # definindo o nome do curso
                                        curso = str(ccdm[j])
                                        result = re.search('titulo=\"(.*)\" titulo-ingl',
                                                        curso)
                                        cc = fun_result(result)
                                        ls_curscd_name.append(cc)
                                        # print(cc)
                                        # definindo o ano do curso
                                        curso = str(ccdm[j])
                                        result = re.search('ano=\"(.*)\" doi',
                                                        curso)
                                        cc = fun_result(result)
                                        ls_curscd_year.append(cc)
                                        # print(cc)
                                        # Integrante do curso
                                        ccdm_aut = ccdm[j].find_all('autores')
                                        ls_all_autor = []
                                        for k in range(len(ccdm_aut)):
                                            autor = str(ccdm_aut[k])
                                            result = re.search(
                                                'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                                                autor)
                                            cc = fun_result(result)
                                            ls_all_autor.append(cc)
                                        # print(ls_all_autor)
                                        ls_curscd_integ.append(ls_all_autor)
                            # DataFrame para cursos de curta duracao
                            df_ccd = pd.DataFrame({'COURSE': ls_curscd_name,
                                                'YEAR': ls_curscd_year,
                                                'INTEGRANTES': ls_curscd_integ})

                            df_ccd_bool=True
                            print(df_ccd)
















































                        cv = soup.find_all('curriculo-vitae')
                        if len(cv) == 0:
                            print('curriculo vitae nao encontrado para', zipname)
                        else:
                            # listas para armazenamento de dados producao tecnica
                            for i in range(len(cv)):
                                dg = cv[i].find_all('dados-gerais')
                                # VERIFICANDO se ha dados gerais
                                if len(dg) == 0:
                                    print('Dados gerais nao encontrados para', zipname)
                                else:
                                    for j in range(len(dg)):
                                        # definindo nome completo
                                        gendata = str(dg[j])
                                        result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                                        gendata)
                                        cc = fun_result(result)
                                        fullname = cc
                        # ------------------------------------------------------------
                        # extrair todas as producoes bibliograficas
                        pb = soup.find_all('producao-bibliografica')
                        # VERIFICANDO se ha demais tipos de producao
                        if len(pb) == 0:
                            print('Producoes bibliograficas nao encontradas para', zipname)
                        else:
                            # Da producao bibliografica extrair o grupo de artigos publicados
                            artspubs = pb[0].find_all('artigos-publicados')
                            # VERIFICANDO se ha artigos publicados
                            if len(artspubs) == 0:
                                print('Artigos publicados nao encontrados para', zipname)
                            else:
                                # listas para armazenamento de dados PERIODICOS
                                ls_per_title = []
                                ls_per_year = []
                                ls_per_doi = []
                                ls_per_lang = []
                                ls_per_journal = []
                                ls_per_issn = []
                                ls_per_qualis = []
                                ls_per_authors = []
                                ls_per_authororder = []
                                ls_per_orders = []
                                ls_jcr = []
                                # A partir do grupo de artigos publicados extrair os artigos
                                # publicados
                                artpub = artspubs[0].find_all('artigo-publicado')
                                # a partir de cada artigo publicado extrair inf de interesse
                                for i in range(len(artpub)):
                                    # dados basicos do paper
                                    dba = artpub[i].find_all('dados-basicos-do-artigo')
                                    paperdb = str(dba)
                                    # definindo o nome do paper
                                    result = re.search('titulo-do-artigo=\"(.*)\" titulo-do-artigo-i',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_title.append(cc)
                                    # print(cc)
                                    # definindo ano do paper
                                    result = re.search('ano-do-artigo=\"(.*)\" doi',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_year.append(cc)
                                    # print(cc)
                                    # definindo doi do paper
                                    result = re.search('doi=\"(.*)\" flag-divulgacao-c',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_doi.append(cc)
                                    # print(cc)
                                    # definindo idioma do paper
                                    result = re.search('idioma=\"(.*)\" meio-de-divulgacao=',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_lang.append(cc)
                                    # print(cc)
                                    # detalhamento do paper
                                    dda = artpub[i].find_all('detalhamento-do-artigo')
                                    paperdt = str(dda)
                                    # definindo titulo do periodico
                                    result = re.search('titulo-do-periodico-ou-revista=\"(.*)\" volume',
                                                    paperdt)
                                    cc = fun_result(result)
                                    ls_per_journal.append(cc)
                                    # print(cc)
                                    # definindo issn
                                    result = re.search('issn=\"(.*)\" local-de-public',
                                                    paperdt)
                                    if result is None:
                                        cc = 'VAZIO'
                                    else:
                                        cc = result.group(1)
                                        cc = str(cc[0:4]) + '-' + str(cc[4:])
                                    ls_per_issn.append(cc)
                                    # print(cc)
                                    # autores do paper
                                    aut = artpub[i].find_all('autores')
                                    ls_allauthors = []
                                    ls_allauthororder = []
                                    ls_authororder = []
                                    for j in range(len(aut)):
                                        auth = str(aut[j])
                                        result = re.search(
                                            'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                                            auth)
                                        if result is None:
                                            cc = 'VAZIO'
                                        else:
                                            cc = result.group(1)
                                            nca = result.group(1)  # nomecompletoautor
                                        ls_allauthors.append(cc)
                                        # print(cc)
                                        # order de autoria
                                        result = re.search(
                                            'ordem-de-autoria=\"(.*)\"',
                                            auth)
                                        if result is None:
                                            cc = 'VAZIO'
                                        else:
                                            cc = result.group(1)
                                            ncao = result.group(1)
                                        ls_allauthororder.append(cc)
                                        if fullname == nca:
                                            ls_authororder.append(ncao)
                                            # print(fullname + ' ' + ncao)
                                        # print(cc)
                                    ls_per_authors.append(ls_allauthors)
                                    ls_per_authororder.append(ls_allauthororder)
                                    ls_per_orders.append(ls_authororder)

                                

                                    # print(cc)
                                # DataFrame periodicos
                                df_papers = pd.DataFrame({'TITLE': ls_per_title,
                                                        'YEAR': ls_per_year,
                                                        'DOI': ls_per_doi,
                                                        'LANG': ls_per_lang,
                                                        'JOURNAL': ls_per_journal,
                                                        'ISSN': ls_per_issn,
                                                        'AUTHOR': ls_per_authors,
                                                        'ORDER': ls_per_authororder,
                                                        'ORDER_OK': ls_per_orders,})
                                df_papers_bool=True
                        





                        

                        
                        cv = soup.find_all('curriculo-vitae')
                        if len(cv) == 0:
                            print('curriculo vitae nao encontrado para', zipname)
                        else:
                            # listas para armazenamento de dados producao tecnica
                            for i in range(len(cv)):
                                dg = cv[i].find_all('dados-gerais')
                                # VERIFICANDO se ha dados gerais
                                if len(dg) == 0:
                                    print('Dados gerais nao encontrados para', zipname)
                                else:
                                    for j in range(len(dg)):
                                        # definindo nome completo
                                        gendata = str(dg[j])
                                        result = re.search('nome-completo=\"(.*)\" nome-em-citacoes',
                                                        gendata)
                                        cc = fun_result(result)
                                        fullname = cc
                        # ------------------------------------------------------------
                        # extrair todas as producoes bibliograficas
                        pb = soup.find_all('producao-bibliografica')
                        # VERIFICANDO se ha demais tipos de producao
                        if len(pb) == 0:
                            print('Producoes bibliograficas nao encontradas para', zipname)
                        else:
                            # Da producao bibliografica extrair o grupo de artigos publicados
                            trabalhobb = pb[0].find_all('trabalhos-em-eventos')
                            # VERIFICANDO se ha artigos publicados
                            
                            
                            if len(trabalhobb) == 0:
                                print('Artigos publicados nao encontrados para', zipname)
                            else:
                                # listas para armazenamento de dados PERIODICOS
                                ls_per_title = []
                                ls_per_year = []
                                ls_per_doi = []
                                ls_per_lang = []
                                ls_per_authors = []
                                ls_per_authororder = []
                                ls_per_orders = []

                                # A partir do grupo de artigos publicados extrair os artigos
                                # publicados
                                trabalhob = trabalhobb[0].find_all('trabalho-em-eventos')
                                # a partir de cada artigo publicado extrair inf de interesse
                                for i in range(len(trabalhob)):
                                    # dados basicos do paper
                                    dba = trabalhob[i].find_all('dados-basicos-do-trabalho')
                                    paperdb = str(dba)
                                    # definindo o nome do paper
                                    result = re.search('titulo-do-trabalho=\"(.*)\" titulo-do-trabalho-i',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_title.append(cc)
                                    # print(cc)
                                    # definindo ano do paper
                                    result = re.search('ano-do-trabalho=\"(.*)\" doi',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_year.append(cc)
                                    # print(cc)
                                    # definindo doi do paper
                                    result = re.search('doi=\"(.*)\" flag-divulgacao-c',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_doi.append(cc)
                                    # print(cc)
                                    # definindo idioma do paper
                                    result = re.search('idioma=\"(.*)\" meio-de-divulgacao=',
                                                    paperdb)
                                    cc = fun_result(result)
                                    ls_per_lang.append(cc)
                                    # print(cc)
                                    # detalhamento do paper
                                    dda = trabalhob[i].find_all('detalhamento-do-trabalho')
                                    paperdt = str(dda)
                                    # definindo titulo do periodico
                                    result = re.search('nome-do-evento=\"(.*)\" volume',
                                                    paperdt)
                                    cc = fun_result(result)
                                    # print(cc)
                                    # definindo issn
                                    result = re.search('cidade-do-evento=\"(.*)\"',
                                                    paperdt)
                                    if result is None:
                                        cc = 'VAZIO'
                                    else:
                                        cc = result.group(1)
                                        cc = str(cc[0:4]) + '-' + str(cc[4:])

                                    # print(cc)
                                    # autores do paper
                                    aut = trabalhob[i].find_all('autores')
                                    ls_allauthors = []
                                    ls_allauthororder = []
                                    ls_authororder = []
                                    for j in range(len(aut)):
                                        auth = str(aut[j])
                                        result = re.search(
                                            'nome-completo-do-autor=\"(.*)\" nome-para-citacao',
                                            auth)
                                        
                                        if result is None:
                                            cc = 'VAZIO'
                                        else:
                                            cc = result.group(1)
                                            nca = result.group(1)  # nomecompletoautor
                                        ls_allauthors.append(cc)
                                        # print(cc)
                                        # order de autoria
                                        result = re.search(
                                            'ordem-de-autoria=\"(.*)\"',
                                            auth)
                                        if result is None:
                                            cc = 'VAZIO'
                                        else:
                                            cc = result.group(1)
                                            ncao = result.group(1)
                                        ls_allauthororder.append(cc)
                                        if fullname == nca:
                                            ls_authororder.append(ncao)
                                            # print(fullname + ' ' + ncao)
                                        # print(cc)
                                    ls_per_authors.append(ls_allauthors)
                                    ls_per_authororder.append(ls_allauthororder)
                                    ls_per_orders.append(ls_authororder)

                                

                                    # print(cc)
                                # DataFrame periodicos
                                df_trabalho = pd.DataFrame({'TITLE': ls_per_title,
                                                        'YEAR': ls_per_year,
                                                        'DOI': ls_per_doi,
                                                        'LANG': ls_per_lang,
                                                        'AUTHOR': ls_per_authors,
                                                        'ORDER': ls_per_authororder,
                                                        'ORDER_OK': ls_per_orders,})
                                df_trabalho_bool=True

                    


                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print()
                        print("STATUS OF ALL THE DATAFRAMES")
                        print('----------------------------------------------------------')
                        print('DF FOR PAPERS',df_papers_bool)
                        print('DF FOR FULLNAME',df_fullname_bool)
                        print('DF FOR PPE ',df_ppe_bool)
                        print('DF FOR ENS',df_ens_bool)
                        print('DF FOR ADVIS',df_advis_bool)
                        print('DF FOR CCD',df_ccd_bool)
                        print ('DF FOR CAPIT',df_capit_bool)
                        print ('DF FOR TRABALHO',df_trabalho_bool)
                        print('Operation starting for',fullname,' in 5 seconds')
                        print()
                        time.sleep(5)


                        if df_capit_bool==True:
                            
                            
                            if df_capit.empty==False:
                                print ('There is some content in DF_Capit for ',fullname)
                                for x,y in df_capit.iterrows():

                                    x1=y['YEAR']
                                    x2=y['LANG']
                                    x3=y['TITLE']
                                    x4=y['AUTHOR']
                                    chapter = CapitulosDeLivrosPublicados(Nome=fullname, Title=x3, Year=x1, Lang=x2, Author=x4)
                                    chapter.save()
                                    


                                    



                        else:
                            print ('The DF of Livros doesnt exist for',fullname)






                        if df_ccd_bool==True:
                            print('----------------------------------------------------------')
                            
                            if df_ccd.empty==False:
                            
                                print ('There is some content in Tech_production for', fullname)
                                for x,y in df_ccd.iterrows():

                                    x1=y['COURSE']
                                    x2=y['YEAR']
                                    x3=y['INTEGRANTES']

                                    
                                        

                                    technical_production = ProducaoTecnica(
                                    Fullname=fullname,
                                    Course=x1,
                                    Year=x2,
                                    Integrantes=x3,
                                
                            )
                                    technical_production.save()
                                 



                            else:
                                print ('no data in ccd')
                        else:
                            print('----------------------------------------------------------')
                            print ('The DF of technical_production doesnt exist for ',fullname)









                        if df_advis_bool==True:
                            print('----------------------------------------------------------')
                            if df_advis.empty==False:
                                print ('There is some content in DF other_production for ', fullname)
                                for x,y in df_advis.iterrows():

                                    x1=y['YEAR']
                                    x2=y['NATURE']
                                    x3=y['COURSE']
                                    x4=y['STUDENT']
                                    x5=y['TYPE']
                                    x6=y['SPONSOR']
                                    x7=y['INSTITUTION']
                                    other_production = OtherProductions(
                                    Fullname=fullname,
                                    YEAR=x1,
                                    NATURE=x2,
                                    INSTITUTION=x7,
                                    COURSE=x3,
                                    STUDENT=x4,
                                    TYPE=x5, 
                                    SPONSOR=x6
                                )
                                    other_production.save()

                                    
                                
                        else:
                            print('----------------------------------------------------------')
                            print ('The DF of other_production doesnt exist for ',fullname)








                        if df_papers_bool==True:
                            print('----------------------------------------------------------')
                            if df_papers.empty==False:
                                print ('There is some content here in publications for ', fullname)
                                for x,y in df_papers.iterrows():

                                    x1=y['TITLE']
                                    x2=y['YEAR']
                                    x3=y['DOI']
                                    x4=y['LANG']
                                    x5=y['JOURNAL']
                                    
                                    x7=y['ISSN']
                                    x8=y['AUTHOR']
                                    publication = Publications(
                                    Fullname=fullname, 
                                    TITLE=x1, 
                                    YEAR=x2,
                                    DOI=x3, 
                                    LANG=x4, 
                                    JOURNAL=x5,
                                    ISSN=x7, 
                                    AUTHOR=x8
                                    )
                                    publication.save()

                                    
                            
                        else:
                            print('----------------------------------------------------------')
                            print ('The DF of publications doesnt exist here for ',fullname)








                        if df_ens_bool==True:
                            print('----------------------------------------------------------')
                            if df_ens.empty==False:
                                print ('There is some content here in Education for ',fullname)
                                for x,y in df_ens.iterrows():

                                    x1=y['YEAR_INI']
                                    x2=y['YEAR_FIN']
                                    x3=y['MONTH_INI']
                                    x4=y['MONTH_FIN']
                                    x5=y['COURSE']
                                    x6=y['TYPE']
                                    x7=y['DISC']
                                    education = Education(
                                    Nome=fullname, 
                                    Year_INI=x1, 
                                    Year_FIN=x2,
                                    Month_INI=x3, 
                                    Month_FIN=x4,
                                    Course=x5, 
                                    Type=x6, 
                                    Discipline=x7
                                    )
                                    education.save()

                                    

                                    
                        else:
                            print('----------------------------------------------------------')
                            print ('The DF of education doesnt exist for',fullname)






                        if df_ppe_bool==True:
                            print('----------------------------------------------------------')

                            if df_ppe.empty==False:
                                print ('There is some content in Project for ',fullname)
                                for x,y in df_ppe.iterrows():

                                    x1=y['PROJ']
                                    x2=y['YEAR_INI']
                                    x3=y['YEAR_FIN']
                                    x4=y['NATUREZA']
                                    x5=y['INTEGRANTES']
                                    x6=y['COORDENA']
                                    project = Project(
                                    Fullname=fullname, 
                                    Proj=x1, 
                                    YEAR_INI=x2,
                                    YEAR_FIN=x3, 
                                    Natureza=x4,
                                    Integrantes=x5, 
                                    Cordena=x6
                                    )
                                    project.save()

                                    
                                    

                                
                        else:
                            print('----------------------------------------------------------')
                            print ('The DF for projects doesnt exist here for',fullname)







                    
                        


                        if df_fullname_bool==True and compare(fullname)==False:
                            print('----------------------------------------------------------')

                            if df_fullname.empty==False:
                                print ('There is some content here for Person for',fullname)
                                for x,y in df_fullname.iterrows():

                                    x1=y['FULL_NAME']
                                    x2=y['FULL_NAME']
                                    x10=y['LAST_NAME']
                                    x3=y['CITADO']
                                    x4=y['CITY']
                                    x5=y['STATE']
                                    x6=y['RESUME']
                                    x7=y['ADDRESS_ENTERP']
                                    x8=y['ORCID']
                                    x9=y['UPDATE']
                                    person = Person(

                                    ID=x1, 
                                    Last_Name=x10,
                                    City=x4, 
                                    State=x5, 
                                    Description=x6,
                                    Workplace=x7,
                                    Update=x9, 
                                    ORCID=x8,
                                    Full_name=x2,
                                    Citation=x3
                                    )
                                    person.save()

                                    

                                    
                                    
                        else:
                            print('----------------------------------------------------------')
                            print ('The DF of Fullname doesnt exist here for ',fullname)
                        if compare(fullname)==True and df_fullname_bool==True:
                            for x,y in df_fullname.iterrows():

                                    x1=y['ID']
                                    x2=y['FULL_NAME']
                                    x10=y['LAST_NAME']
                                    x3=y['CITADO']
                                    x4=y['CITY']
                                    x5=y['STATE']
                                    x6=y['RESUME']
                                    x7=y['ADDRESS_ENTERP']
                                    x8=y['ORCID']
                                    x9=y['UPDATE']
                            update_person_with_django_by_fullname(x2,x10,x3,x4,x5,x6,x7,x9,x8)
                            print("user already exists. Run update") 

 
                        if df_trabalho_bool==True:
                            print('----------------------------------------------------------')
                            if df_trabalho.empty==False:
                                print ('There is some content here in Trabalhos for ',fullname)
                                for x,y in df_papers.iterrows():


                                    x1=y['TITLE']
                                    x2=y['YEAR']
                                    x3=y['DOI']
                                    x4=y['LANG']
                                    x5=y['AUTHOR']
                                    x6=y['ORDER']
                                    x7=y['ORDER_OK']
                                    trabalho = Trabalho(
                                    fullname=fullname,
                                    TITLE=x1, 
                                    YEAR=x2,
                                    DOI=x3, 
                                    LANG=x4, 
                                    AUTHOR=x5,
                                    ORDER=x6,
                                    ORDER_OK=x7
                                    )
                                    trabalho.save()

                                
                            
                        else:
                            print('----------------------------------------------------------')
                            print ('The DF of trabalhos doesnt exist for ',fullname)