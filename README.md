# Logement IoT

Dossier présentant mon travail concernant le TP logement éco responsable proposé.

Tout d'abord pour faire fonctionner le tout, il faut, dans un terminal, exécuter les commandes suivantes (recommandé de le faire dans un environnement virtuel) : 

pip install requests
pip install requests

Ensuite, je tiens à préciser que le rendu est divisé en 4 sous-dossier reprenant le travaiul fait lors des séances 1 à 4. Par conséquent, les fichiers sont modifiés d'un TP à l'autre et peuvent également accumuler le travail réalisé lors de TP précédent. De plus, dans le cadre de ce devoir, chatGPT a été utilisé.

Concernant l'exercice 1, les réponses sont disponible dans le dossier TP1, le fichier logement.sql correspond à toutes les réponses jusqu'à la question 8 du 1,1.? Le fichier python répond au 1.2.

Pour l'exercice 2, les réponses se trouvent dans le fichier remplissage.py. La question 1 trouve sa réponse entre les lignes 15 et 170. 
Question 2 : entre les lignes 171 et 262. ChatGPT a été utilisé pour la génération de la page html et l'utilisation de google.
Question 3 : Pour afficher la météo, la réponse se trouve entre les lignes 264 et 370. 
Question 4 : Une partie ESP existe mais je ne suis pas allé plus loin car je n'avais pas le matériel.

Concernant l'exercice 3, une avancée est visible dans le dossier TP3 mais comme celui-ci represente l'ensemble du travail effectué, regardons le dossier TP4.
Pour lancer le serveur, il faut aller dans le dossier Logement dans un terminal et lancer la commande python remplissage.py
L'idée que j'ai eu afin de rendre ça plus "original" était non pas de regrouper des la gestion de logement factice mais de mettre ça en place pour diverses campus de Sorbonne Université.
Dans notre cas, étant au stade de prototype, je me suis contenté de 2 campus. Nous pouvons ajouter:supprimer des capteurs et des factures, visualiser l'emplacement du campus sur une carte avec des prévisions météos.
Le code générant le serveur se trouve toujours dans remplissage.py, les différentes routes flask se troue-vent entre les lignes 373 et 737 (pas mal de lignes de codes ont été reprises des exercices précédents mais j'ai fait le choix de tout garder dans ce même fichier afin de "suivre" le sujet. Les pages HTML correspondantes se trouvent dans un dossier nommé "Template". Concernant le javascript, je n'ai pas fait de fichier js, j'ai directement codé dans le fichier HTML correspondant à chacune des pages, les script sont visibles à partir des balises si bien nommé... <script>. Pour cette partie HTML, j'ai pas mal utilisé chatGPT afin d'avoir un rendu cohérent avec Boostrap.

Merci de votre lecture, je vous laisse maintenant avec les différents fichiers.
