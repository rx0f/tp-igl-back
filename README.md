<h2>ISTATE</h2>
Une application Web pour la publication et la consultation des annonces immobilières les plus récentes. 
Les utilisateurs pourront publier leurs propres annonces ainsi que visualiser celles publiées par d’autres utilisateurs ou provenant d’autres sites d’annonces. 
Cette application sera un moyen pratique pour trouver les dernières annonces immobilières et publier les propres aisément. 
En fin de compte, elle am´eliorera la communication et la transparence sur le march´e immobilier.


<p>Ce repository contient le code source pour le backend d'une application web développé avec Flask. Il inclut une base de données SQLite, un code de scrapping "scrapper.py" fait avec BeautifulSoup, l'authentification par Google OAuth2 et trois tests unitaires. Le backend est déployé sur Render.</p>

<h2>Installation des dépendances</h2>
<ol>
  <li>Clonez ce repository sur votre ordinateur</li>
  <li>Naviguez à l'intérieur du répertoire cloné</li>
  <li>Installer les dépendences necessaires qui se trouvent dans le fichier `requirements.txt`</li>
</ol>
<h2>Base de données</h2>
<ul>
  <li>La base de données SQLite se trouve dans le dossier `instance`</li>
  <li>Vous pouvez utiliser un outil de gestion de base de données SQLite pour interagir avec la base de données</li>
</ul>
<h2>Scrapper</h2>
<ul>
  <li>Le code de scrapping se trouve dans le fichier `scrapper.py`</li>
  <li>Il peut être exécuté indépendamment pour effectuer le scrapping</li>
</ul>
<h2>Tests unitaires</h2>
<ul>
  <li>Les tests unitaires se trouvent dans le dossier `test`</li>
  <li>Vous pouvez exécuter les tests avec la commande `python -m pytest`</li>
</ul>
<h2>Développement local</h2>
<ol> 
  <li>Démarrez le serveur local avec la commande `flask run`</li>
  <li>Accédez à l'application à l'adresse convenable sur votre navigateur</li>
</ol>

<h2>Remarques</h2>
<p>Veuillez n'hésiter à consulter la documentation de Flask, SQLite, BeautifulSoup, Google OAuth2 et Render</p>

<h2>Déploiement</h2>
<p>Le backend est déployé sur https://tp-igl-back.onrender.com/</p>

Enjoy!
