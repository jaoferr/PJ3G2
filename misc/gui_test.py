#!pip install PySimpleGUI

import PySimpleGUI as sg 

class TelaPython:
    def __init__(self):
        sg.change_look_and_feel('LightBlue3') # mudar o design
        #layout
        layout = [
            [sg.Text('Palavra-chave', size=(5,0)),sg.Input(size=(50,0), key='Palavra-chave')], # empresa
            [sg.Text('Base de dados', size=(5,0)),sg.Input(size=(50,0), key='Base de dados')], # base de dados
            [sg.Text('Escolha a área de atuação para a sua vaga:')], # selecione ums area
            [sg.Checkbox('Aplicação de lei',key='Aplicação de lei'), sg.Checkbox('T.I',key='T.I'), sg.Checkbox('RH',key='RH'), sg.Checkbox('Arquitetura',key='Arquitetura'), sg.Checkbox('Trabalho Social',key='Trabalho Social'),  sg.Checkbox('Educação e Treinamento',key='Educação e Treinamento'), sg.Checkbox('Saúde',key='Saúde'), sg.Checkbox('Finança e Contabilidade',key='Finança e Contabilidade'), sg.Checkbox('Manufatura',key='Manufatura'), sg.Checkbox('Turismo e Hospitalidade',key='Turismo e Hospitalidade'), sg.Checkbox('Marketing e Administração',key='Marketing e Administração')], # areas
            [sg.Text('Aceita utilizar as palavras chaves da Grace?')],
            [sg.Radio('Sim','dados', key='aceitoPalavra'),sg.Radio('Não','dados', key='naoAceitoPalavra')], # botão texto e qual grupo pertence
            #[sg.Slider(range=(0,255),default_value=0,orientation='h',size=(15,20),key='sliderVelocidade')],
            [sg.Button('Buscar')], # buscar
            #[sg.Output(size=(30,20))] # mostrar as informações preenchidas para o usuario

        ]

        #janela

        self.janela = sg.Window('GRACE - Assistente de recrutamento').layout(layout)

        #extrair dados da tela 

        #self.button, self.values = self.janela.Read()

    def Iniciar(self): # imprir informações inseridas na tela
        #print(self.values)
        while True: # para não fechar a tela depois que enviar 
            self.button, self.values = self.janela.Read()
            palavra_chave = self.values['Palavra-chave']
            base_de_dados = self.values['Base de dados']
            aceita_aplicação_de_lei = self.values['Aplicação de lei']
            aceita_TI= self.values['T.I']
            aceita_RH = self.values['RH']
            aceita_arquitetura = self.values['Arquitetura']
            aceita_trabalhoSocial = self.values['Trabalho Social']
            aceita_educaçaoeTreinamento = self.values['Educação e Treinamento']
            aceita_saude = self.values['Saúde']
            aceita_finançaeContabilidade = self.values['Finança e Contabilidade']
            aceita_manufatura = self.values['Manufatura']
            aceita_turismo = self.values['Turismo e Hospitalidade']
            aceita_adm = self.values['Marketing e Administração']
            aceita_p_sim = self.values['aceitoPalavra']
            nao_aceita_p = self.values['naoAceitoPalavra']
            #velocidade_script = self.values['sliderVelocidade']
            print(f'Palavra-chave: {palavra_chave}')
            print(f'Base de dados: {base_de_dados}')
            print(f'Aplicação de lei: {aceita_aplicação_de_lei}')
            print(f'T.I: {aceita_TI}')
            print(f'RH: {aceita_RH}')
            print(f'Arquitetura: {aceita_arquitetura}')
            print(f'Trabalho Social: {aceita_trabalhoSocial}')
            print(f'Educação e Treinamento: {aceita_educaçaoeTreinamento}')
            print(f'Saúde: {aceita_saude}')
            print(f'Finança e Contabilidade: {aceita_finançaeContabilidade}')
            print(f'Manufatura: {aceita_manufatura}')
            print(f'Turismo e Hospitalidade: {aceita_turismo}')
            print(f'Marketing e Administração: {aceita_adm}')
            print(f'Aceito palavra:{aceita_p_sim}')
            print(f'Não aceito palavra:{nao_aceita_p}')
            #print(f'velocidade script:{velocidade_script}')

tela = TelaPython()
tela.Iniciar()

