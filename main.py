from jinja2 import Template
from ipaddress import IPv4Address

def crear_valores_jinja(line):

    subnet = IPv4Address(line[4])
    mgmt_ip = subnet + 254
    usuarios_ip = subnet + 1

    valores = {
        "HOSTNAME" : line[0] + line[1] + 'RTR' + line[3],
        "IP_MGMT" : mgmt_ip,
        "IP_DATOS" : usuarios_ip,
        "DATA_HELPER" : ['172.18.25.1','172.18.26.2','172.18.27.3'],
        "SUBNET_SITIO" : subnet,
        "IP_SYSLOG_N" : '192.168.10.254',
        "IP_SYSLOG_S" : '192.168.33.1'
    }

    return valores


def crear_jinja_data(plantilla,valores):

    with open(plantilla,'r') as j:

        plantilla_jinja = Template(j.read())
        jinja_data = plantilla_jinja.render(valores)

    return jinja_data


def crear_archivo_config(valores,jinja_data):

    archivo = valores["HOSTNAME"] + '.txt'

    with open(f'configs/{archivo}','w') as f:
        for line in jinja_data:
            f.write(line)


def main():

    with open('docs/info_sucursales.csv') as d:

        for row in d:
            clean_row = row.replace('\n', '')
            line = clean_row.split(',')

            if line[0] != 'PAIS':

                try:

                    valores = crear_valores_jinja(line)
                    jinja_data = crear_jinja_data('docs/plantilla_config.j2',valores)
                    crear_archivo_config(valores,jinja_data)

                except:
                    print(f'ADVERTENCIA! Problemas en la linea {line}')

    print('Trabajo finalizado!')


if __name__ == '__main__':
    main()
