import PyPDF2
import pandas as pd
import re

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        all_data = []
        for page_num in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page_num].extract_text()
            print(f'Verificando página: {page_num + 1}...')
            
            funcionario_indices = [m.start() for m in re.finditer("Funcionário:", text)]
            
            for index in funcionario_indices:
                data = process_text(text[index:])
                all_data.append(data)
    
    return all_data

def has_information(text):
    keywords = ["Funcionário:"]
    
    for keyword in keywords:
        if keyword in text:
            return True
    
    return False

def get_value_by_funcionario(text):
    funcionario_id, funcionario_nome = "", ""
    keyword = "Funcionário:"
    
    if keyword in text:
        start_index = text.find(keyword) + len(keyword)
        funcionario_info = text[start_index:text.find('\n', start_index)].strip()
        
        if "Dias F.Venc: 0" in funcionario_info:
            funcionario_info = funcionario_info.replace("Dias F.Venc: 0", "")
        
        funcionario_split = funcionario_info.split('-')
        
        if len(funcionario_split) == 2:
            funcionario_id, funcionario_nome = map(str.strip, funcionario_split)
    
    return funcionario_id, funcionario_nome


def get_value_by_dias_fvenc(text):
    dias_fvenc_value = ""
    keyword = "Dias F.Venc:"
    
    if keyword in text:
        start_index = text.find(keyword) + len(keyword)
        dias_fvenc_value = re.search(r'\d+', text[start_index:]).group()
    
    return dias_fvenc_value

def get_value_by_dias_fprop(text):
    keyword = "Dias F.Prop:"
    dias_fprop = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(2):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        dias_fprop = text[start_index:end_index].strip()

        dias_fprop = dias_fprop[-4:]

    return dias_fprop

def get_value_by_avos_fprop(text):
    keyword = "Avos F.Prop:"
    avos_fprop = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(2):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        avos_fprop = text[start_index:end_index].strip()

    return avos_fprop

def get_value_by_ult_ferias(text):
    keyword = "Ult.Férias:"
    date_pattern = r'\b\d{2}/\d{2}/\d{4}\b'

    ult_ferias_date = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)
        match = re.search(date_pattern, text[start_index:])

        if match:
            ult_ferias_date = match.group()

    return ult_ferias_date

def get_value_by_ferias_venc(text):
    keyword_start = "Férias Venc:"
    keyword_end = "FGTS"
    ferias_venc_value = ""

    start_index = text.find(keyword_start)
    end_index = text.find(keyword_end, start_index)

    if start_index != -1 and end_index != -1:
        start_index += len(keyword_start)
        ferias_venc_text = text[start_index:end_index].strip()

        # Pega após "Férias Venc:"
        match = re.search(r'(\d{1,3}(?:[\.,]\d{3})*(?:[\.,]\d{2})?)', ferias_venc_text)

        if match:
            ferias_venc_value = match.group(1).replace(".", "").replace(",", ".")

    return ferias_venc_value
#1=Adc.Fer.Vnc:/#2=Fer. Prop:/3=Prop:(Adc.Fer.Vnc:)/4=Venc:(Fer. Prop:)/5=?
def get_value_by_venc_linha_feriasvenc(text):
    keyword = "Férias Venc:"
    venc_linha_feriasvenc = []

    lines = text.splitlines()

    for i, line in enumerate(lines):
        if keyword in line:
            # Captura os 5 conjuntos de caracteres após "Férias Venc:"
            for j in range(i + 1, i + 6):
                if 0 <= j < len(lines):
                    venc_linha_feriasvenc.append(lines[j].strip())

    # Verifica se tem pelo menos dois itens na lista
    if len(venc_linha_feriasvenc) >= 2:
        # Retorna o segundo item (índice 1) após o espaço
        return venc_linha_feriasvenc[1].split()[1] if ' ' in venc_linha_feriasvenc[1] else None
    else:
        return None


def get_value_by_adc_fer_venc(text):
    keyword = "Férias Venc:"
    adc_fer_venc_value = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(1):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        venc_value = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)', text[start_index:end_index])
        
        if venc_value:
            adc_fer_venc_value = venc_value.group(1).replace(".", "").replace(",", ".")
        
    return adc_fer_venc_value

def get_value_by_prop_linhaadcfervnc(text):
    keyword = "Férias Venc:"
    prop_linhaadcfervnc_value = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(3):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        prop_linhaadcfervnc_value = text[start_index:end_index].strip()
        
    return prop_linhaadcfervnc_value

def get_value_by_fer_prop(text):
    keyword = "Férias Venc:"
    fer_prop_value = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(2):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        fer_prop_value = text[start_index:end_index].strip()
        match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2}))', fer_prop_value)
        fer_prop_value = match.group(1).replace(".", "").replace(",", ".")
        
    return fer_prop_value

def get_value_by_venc_linha_ferprop(text):
    keyword = "Férias Venc:"
    venc_linha_ferprop = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(4):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        venc_linha_ferprop = text[start_index:end_index].strip()
        match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d{2}))', venc_linha_ferprop)
        venc_linha_ferprop = match.group(1).replace(".", "").replace(",", ".")

    return venc_linha_ferprop

def get_value_by_ad_fer_prop(text):
    keyword = "Salário Mensal.:"
    ad_fer_pro_value = []

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)
        ad_fer_pro_value = text[start_index:].split()
        ad_fer_pro_value = ad_fer_pro_value[21]

    return ad_fer_pro_value

def get_value_by_prop_adferpro(text):
    keyword = "Salário Mensal.:"
    prop_adferpro_value = []

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)
        prop_adferpro_value = text[start_index:].split()
        prop_adferpro_value = prop_adferpro_value[23]

    return prop_adferpro_value

def get_value_by_salario_mensal(text):
    keyword = "Salário Mensal.:"
    salario_mensal_value = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(12):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        salario_mensal_value = text[start_index:end_index].strip()

    return salario_mensal_value

def get_value_by_salario_refer(text):
    keyword = "Salário Refer..:"
    salario_refer_value = ""

    if keyword in text:
        start_index = text.find(keyword) + len(keyword)

        for _ in range(12):
            start_index = text.find('\n', start_index) + 1
        
        end_index = text.find('\n', start_index)

        salario_refer_value = text[start_index:end_index].strip()
        salario_refer_value = salario_refer_value = text[start_index:].split()[0]
    
    return salario_refer_value

def process_text(text):
    funcionario_id, funcionario_nome = get_value_by_funcionario(text)
    dias_fvenc_value = get_value_by_dias_fvenc(text)
    dias_fprop_value = get_value_by_dias_fprop(text)
    avos_fprop_value = get_value_by_avos_fprop(text)
    ult_ferias_value = get_value_by_ult_ferias(text)
    ferias_venc_value = get_value_by_ferias_venc(text)
    venc_linha_feriasvenc_value = get_value_by_venc_linha_feriasvenc(text)
    adc_fer_venc_value = get_value_by_adc_fer_venc(text)
    venc_linha_ferprop = get_value_by_venc_linha_ferprop(text)
    prop_linhaadcfervnc_value = get_value_by_prop_linhaadcfervnc(text)
    fer_prop_value =  get_value_by_fer_prop(text)
    ad_fer_pro_value = get_value_by_ad_fer_prop(text)
    prop_adferpro_value = get_value_by_prop_adferpro(text)
    salario_mensal_value = get_value_by_salario_mensal(text)
    salario_refer_value = get_value_by_salario_refer(text)

    print(f"Funcionário ID: {funcionario_id}, AD FER PROP: {ad_fer_pro_value}, PROP: { prop_adferpro_value}")

    data = {
        "ID": funcionario_id,
        "NOME": funcionario_nome,
        "DIAS F. VENC.": dias_fvenc_value,
        "DIAS F. PROP.": dias_fprop_value,
        "AVOS F. PROP.": avos_fprop_value,
        "ULT. FÉRIAS": ult_ferias_value,
        "FÉRIAS VENC.": ferias_venc_value,
        "VENC (FÉRIAS VENC)": venc_linha_feriasvenc_value,
        "ADC. FER. VENC.": adc_fer_venc_value,
        "PROP (ADC.FER.VNC)":prop_linhaadcfervnc_value,
        "FER. PROP:": fer_prop_value,
        "VENC (FER. PROP.)": venc_linha_ferprop,
        "AD. FER. PROP": adc_fer_venc_value,
        "PROP (AD. FER. PROP)": prop_adferpro_value,
        "SALÁRIO MENSAL": salario_mensal_value,
        "SALÁRIO REFER": salario_refer_value,
    }
    return data

pdf_path = r'D:\1Desktop\Documentos\My Web Sites\App py\Dados de Férias e Salário de PDF\PROVISAO FERIAS COMPLETA 112023 PDF.pdf'
all_data = extract_text_from_pdf(pdf_path)
df = pd.DataFrame(all_data)

excel_path = r'D:\1Desktop\Documentos\My Web Sites\App py\Dados de Férias e Salário de PDF\Provisão Férias Geral.xlsx'
df.to_excel(excel_path, index=False)

print(f'Dados salvos em {excel_path}')