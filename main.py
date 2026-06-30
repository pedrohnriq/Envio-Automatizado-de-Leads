import os
from datetime import datetime, timedelta
from e_leads_edt import leads_edt
from l_email import Email


def main():
    data_ontem = (
        datetime.now() - timedelta(days=1)
    ).strftime("%Y-%m-%d")

    arquivo_relatorio = f"Leads EDT {data_ontem}.xlsx"

    # Extrai/gera o relatório
    leads_edt()

    if not os.path.exists(arquivo_relatorio):
        print(f"Arquivo não encontrado: {arquivo_relatorio}")
        return

    email_sender = Email()

    destinatarios = ["fernando.santos@energiadetodos.com.br", 
                     "planejamento@energiadetodos.com.br", 
                     "lucas.alves@energiadetodos.com.br"
    ]

    copia = ["pedrooliveira@cartaodetodos.com", 
             "leonardo.rocha@energiadetodos.com.br", 
             "cassioluizdasilva@cartaodetodos.com"]

    assunto = f"Relatório Diário EDT - {data_ontem}"

    hoje = datetime.now() 
    if hoje.weekday() == 0: # segunda-feira = 0 
        corpo = "Prezados,\nSegue em anexo o relatório Leads EDT do Cartão de Todos referente ao fim de semana." \
        "\nAtenciosamente, Tech TODOS." 
        anexo = [f"Leads EDT {data_ontem}.xlsx"] 
    
    else: corpo = "Prezados,\nSegue em anexo o relatório de Leads EDT do Cartão de Todos referente à data de ontem." \
    "\nAtenciosamente, Tech TODOS." 
    anexo = [f"Leads EDT {data_ontem}.xlsx"]

    email_sender.send_email(
        to=destinatarios,
        subject=assunto,
        body=corpo,
        attachments=[arquivo_relatorio],
        cc=copia
    )


if __name__ == "__main__":
    main()