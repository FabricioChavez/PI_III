parameter = '0b0563f4-9f97-44d9-b9f4-5bf43e20ffaf_Neko.jpeg'

def spliter(string):
    container=parameter.split('_')
    tenant_id = container[-1].split('.')[0]
    print(tenant_id)


if __name__=="__main__":
    spliter(parameter)