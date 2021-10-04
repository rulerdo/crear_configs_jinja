from jinja2 import Template
from ipaddress import IPv4Address

def crear_valores_jinja(linea):

    subnet = IPv4Address(linea[4])
    mgmt_ip = subnet + 254
    usuarios_ip = subnet + 1

    valores = {

        "HOSTNAME" : linea[0] + linea[1] + 'RTR' + linea[3],
        "IP_MGMT" : mgmt_ip,
        "IP_DATOS" : usuarios_ip,
        "DATA_HELPER" : ['172.18.25.1','172.18.26.2','172.18.27.3'],
        "SUBRED_SITIO" : linea[4],
        "REGION" : linea[2],
        "IP_SYSLOG_N" : '192.168.10.254',
        "IP_SYSLOG_S"  : '192.168.33.1',
    }

    return valores


def crear_config_jinja(plantilla,valores):

    with open(plantilla,'r') as j:

        plantilla_jinja = Template(j.read())
        jinja_data = plantilla_jinja.render(valores)

    archivo = valores["HOSTNAME"] + '.txt'

    with open(f'configs/{archivo}','w') as f:

        for line in jinja_data:
            f.write(line)


def main():

    with open('docs/info_sucursales.csv','r') as d:

        for row in d:
            clean_row = row.replace('\n','')
            linea = clean_row.split(',')
            
            if linea[0] != 'PAIS':

                try:

                    valores = crear_valores_jinja(linea)
                    crear_config_jinja('docs/plantilla_config.j2',valores)

                except:
                    print('ADVERTENCIA: Problemas con la linea: ' , linea)

    print('Trabajo Finalizado!')

if __name__ == '__main__':
    main()