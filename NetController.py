
import json
import requests
from requests.structures import CaseInsensitiveDict
api_url = "http://localhost:58000/api/v1/ticket"


def tiket():
    user = input("Username: ")
    paswd = input("Password: ")
    body_parameter = {
    "username" : user,
    "password": paswd
    }
    resp = requests.post(api_url, json.dumps(body_parameter), headers = {"content-type": "application/json"}, verify=False)
    respon_json = resp.json()
    # print(respon_json)
    if resp.status_code == 200:
        print("Tiket anda: ",respon_json["response"]["serviceTicket"])
    elif resp.status_code == 201:
        print("Sesi anda masih aktif")
        print("Tiket anda: ",respon_json["response"]["serviceTicket"])
    else:
        print("Maaf username/password/koneksi gagal")
   

def perangkat_jaringan_full(tiket):
    api_url_getPerangkat = "http://localhost:58000/api/v1/network-device"
    token = tiket
    headers={"X-Auth-Token": token}
    resp = requests.get(api_url_getPerangkat , headers=headers, verify=False)
    print("Request status: ", resp.status_code)
    response_json = resp.json()
    Data_NetDevice = response_json["response"]
    for device in Data_NetDevice:
        print(device["hostname"],(10-len(device["hostname"]))*' '," | Status: ",device["inventoryStatusDetail"],(10-len(device["inventoryStatusDetail"]))*' '," | IP SSH: ",device["managementIpAddress"],(16-len(device["managementIpAddress"]))*' ',device["type"])


def Peformajaringan(tiket):
    api_url_health = "http://localhost:58000/api/v1/network-health"
    token = tiket
    get_issue = requests.get(api_url_health, headers={"X-Auth-Token":token})
    data = get_issue.json()
    print("Kondisi Perangkat Jaringan :",data["healthyNetworkDevice"],"%")
    print("Kondisi Perangkat Client :",data["healthyClient"],"%")
    print("Banyaknya Switch :",data["numLicensedSwitches"])
    print("Banyaknya Router :",data["numLicensedRouters"])
    print("Perangkat Jaringan yang tidak bisa dijangkau:",data["numUnreachable"])


def NetHealth(tiket):
    api_url_assurance_health = "http://localhost:58000/api/v1/assurance/health"
    token = tiket
    get_issue = requests.get(api_url_assurance_health, headers={"X-Auth-Token":token})
    data_raw = get_issue.json()
    data = data_raw["response"][0]
    data_client = data['clients']
    data_netdevide = data["networkDevices"]["networkDevices"]
    print("Total client:",data_client ["totalConnected"],'perangkat dan ',data_client ["totalPercentage"],
    '%',"terhubung")
    print("Perangkat",'\t','Status','\t','Rasio','\t',"Keterangan")
    for i in data_netdevide:
        print(i["deviceType"],'\t',i["healthyPercentage"],'\t','\t',i["healthyRatio"],'\t',i["healthyRatio"][0],"aktif dari",i["healthyRatio"][2]," Perangkat yang ada")
    
def Masalah_Jaringan(tiket):
    api_url_issue_health = "http://localhost:58000/api/v1/assurance/health-issues"
    token = tiket
    get_issue = requests.get(api_url_issue_health, headers={"X-Auth-Token":token})
    print(get_issue.status_code)
    data_raw = get_issue.json()

    if len(data_raw) >= 2:
        data = data_raw["response"]
        for masalah in data:
            print(masalah["issueSource"],masalah["issueDescription"],masalah["issueName"],masalah["issueTimestamp"],"Kode Masalah",masalah["issueId"])

    else:
        print("Tidak ada masalah yang terjadi")

print("REST API")
tiketing = input("Apakah anda sudah punya tiket? (y/n)")
if tiketing == 'n' or tiketing == 'N':
    konfirm_buat = input("Mau buat tiket?(y/n)")
    if konfirm_buat == 'y' or konfirm_buat == 'Y':
        tiket()
    else:
        print("Bye")
elif tiketing == 'y' or tiketing == 'Y':
    tiket_user = input("Masukan Tiket Anda: ")
    tes_tiket = "http://localhost:58000/api/v1/network-device"
    headers={"X-Auth-Token": tiket_user}
    resp = requests.get(tes_tiket , headers=headers, verify=False)
    if resp.status_code == 200:
        status = True

        while status:
            print("Menu yang tersedia")
            print("1.Peforma Jaringan")
            print("2.Kesehatan Jaringan")
            print("3.Perangkat Jaringan FULL")
            print("4.Cek Masalah Jaringan")
            print("5.Keluar")
            pilihan = int(input("Masukan Pilihan Anda: "))
            if pilihan == 1:
                print('\n'),print('='*15,'Hasil','='*15),print('\n')
                Peformajaringan(tiket_user)
                print('\n'),print('='*15,'Akhir','='*15),print('\n')
            elif pilihan == 2:
                print('\n'),print('='*15,'Hasil','='*15),print('\n')
                NetHealth(tiket_user)
                print('\n'),print('='*15,'Akhir','='*15),print('\n')
            elif pilihan == 3:
                print('\n'),print('='*15,'Hasil','='*15),print('\n')
                perangkat_jaringan_full(tiket_user)
                print('\n'),print('='*15,'Akhir','='*15),print('\n')
            elif pilihan == 4:
                print('\n'),print('='*15,'Hasil','='*15),print('\n')
                Masalah_Jaringan(tiket_user)
                print('\n'),print('='*15,'Akhir','='*15),print('\n')
            elif pilihan == 5:
                print("Bye")
                status = False
            else:
                print("Pilihan anda tidak sesuai")

    else:
        print("emmmm tiket anda salah atau koneksi anda yang salah")
    
else:
    print("Maaf jawaban anda tidak sesuai")


#Abi Fadri | KELAS D | DTS-TSA