from bs4 import BeautifulSoup
import requests


def print_list(items_list):
    for item in items_list:
        print(item)


def print_list_strings(items_list):
    for item in items_list:
        print(item.string)


Wilayas = ["    Adrar     ", "     chlef    ", "   Laghouat   ", "Oum-El-bouaghi", "     Batna    ", "    Bejaia    ",
           "    Biskra    ", "    Bechar    ", "    Blida     ", "    Bouira    ", "  Tamanrasset ", "   Tebessa    ", "    Tlemcen   ",
           "     Tiaret   ", "  Tizi-Ouzou  ", "     Alger    ", "    Djelfa    ", "     Jijel    ", "     Setif    ", "     Saida    ",
           "    Skikda    ", "Sidi-Bel-Abbes", "    Annaba    ", "    Guelma    ", " Constantine  ", "     Medea    ", "  Mostaganem  ",
           "    M-Sila    ", "   Mascara    ", "   Ouargla    ", "     Oran     ", "   El-Bayadh  ", "     Illizi   ", " B-B-Arreridj ",
           "  Boumerdes   ", "    El-Tarf   ", "    Tindouf   ", "  Tissemsilt  ", "   El-Oued    ", "  Khenchela   ", "  Souk-Ahras  ", "    Tipaza    ", "     Mila     ", "   Ain-Defla  ", "     Naama    ", "Ain-temouchent", "   Ghardaia   ",
           "   Relizane   "]


url = "https://www.beytic.com/annonces-immobilieres/?_page={}"
annonce = dict()
list_annonces = list()


for page_number in range(1, 2):
    page_url = url.format(page_number)
    result = requests.get(url)
    status_code = result.status_code
    print(status_code)
    result_text = result.text

    page = BeautifulSoup(result_text, "lxml")
    # getting the items list container
    list_container = page.find(
        "div", class_=["listing", "listing--list"])

    # getting the items list
    list_items = list_container.find_all(
        "div", class_=["listing__item"], limit=3)

    for item in list_items:

        details_link = item.find("a", class_=["item-photo"])
        details_page_href = details_link['href']
        # getting the "id" info
        annonce_id = int(details_page_href.split("/")[4].split("-")[0])
        annonce['id'] = annonce_id
        # now we move to the details page
        details_page = BeautifulSoup(
            requests.get(details_page_href).text, "lxml")
        details_section = details_page.find(class_="property")
        # getting the "price" info
        price = (details_section.find(
            "strong", class_="property__price-value")).string.strip()
        annonce['price'] = price
        # getting the "surface" info
        surface = (details_section.find(
            class_=["property__plan-item"])).find(class_=["property__plan-value"]).string.strip()
        annonce['surface'] = surface
        # getting the photos
        photos = (details_section.find_all(
            class_=["slider__img", "js-gallery-item"]))
        images = []
        url = "https://www.beytic.com///{}"
        for image in photos:
            img_src = image.find("img")
            images.append(url.format(img_src['src']))
        URLs = set(images)

        images = list(URLs)
        annonce['photos'] = images
        # getting the "commission date" info
        publication_date = (details_section.find(
            "h4", class_="property__commision")).string.strip()
        annonce['commision_date'] = publication_date
        # getting the "category" info
        category = (details_section.find(
            "div", class_="property__ribon")).string.strip()
        annonce['category'] = category
        # getting the "type" info
        annonce_type = details_section.find_all(
            class_=["property__info-item"])[0].strong.string.strip()
        annonce['type'] = annonce_type
        # getting the "location" info
        location = details_section.find_all(
            class_=["property__info-item"])[1].div.find_all("a")
        wilaya = location[0].strong.string
        commune = location[1].string.strip()
        # getting the "adress" info
        adresse = details_section.find(
            class_=["property__params"]).li.strong.string.strip()
        locationAdress = {
            'wilaya': wilaya,
            'commune': commune,
            'adresse': adresse
        }
        annonce['locationAdress'] = locationAdress
        # getting the "description" info
        description = details_section.find(
            class_=["property__description"]).div.p.string.strip()
        annonce['description'] = description
        # getting the "contact" info
        sidebar_contact = details_page.find(
            "div", class_=["sidebar", "contact"])
        contact_name = sidebar_contact.find(
            "h3", class_=["worker__name"]).a.string.strip()
        tel_section = sidebar_contact.find(
            class_=["tel"], id="phoneDiv").contents
        phoneNumber = tel_section[2].strip()
        contact = {
            'name': contact_name,
            'phone_number': phoneNumber
        }
        annonce['contact'] = contact

        list_annonces.append(annonce)
        annonce = dict()
    #         # for field in annonce:
    #         #     print(field, ":", annonce[field])


print_list(list_annonces)
