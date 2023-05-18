# Comment utiliser notre application

## Comment clone le projet ?

Pour clone le projet, allez dans votre terminal, mettez vous à l'endroit où vous souhaitez copier le dépot, puis entrer la commande

### `git clone https://github.com/MunHaxx/ThiChaAuLe.git`

Ensuite, vous pouvez entrer dans le répertoire "ThiChaAuLe" et installer les packages nodes-modules avec la commande

### `npm install`

<br><br>

## Comment lancer le projet ?
Pour lancer le projet, il suffit de lancer le script Bash présent dans le répertoire. 

Pour les utilisateurs de Mac, le script permettra de mettre à jour et lancer le projet tout seul. Executer donc la commande :

### `./startRiche.sh`

Et pour les utilisateurs windows, le script permet seulement de mettre à jour le front :
### `.\startPauvre.cmd`

Vous pouvez donc executer la commande précédente, puis lancer le projet comme vous le souhaitez, soit avec la commande "flask run", soit avec pyCharm.


<br><br>

## Comment lancer seulement le front du projet ?
Cependant, si on veut juste lancer l'application front, ça peut se faire en exécutant la commande suivante :

### `npm start` 

<br><br>

## Comment coder ?
Créer une branche sur votre projet dépot local en faisant 
### `git branch maBranche`

Puis déplacez vous sur cette branche en faisant

### `git checkout maBranche`

Désormais, vous pouvez coder, et tous les commits que vous ferez seront sauvegarder sur cette branche.

<br><br>

## Comment commit ?

Pour commit sur VsCode il faut cliquer sur le petit icone représentant des branches git à gauche. Ensuite, e choisir les fichiers à "staged" en cliquant sur le plus (ce sont les fichiers qui seront commit). Après cela, mettez un message qui décrit au mieux votre commit. Enfin, vous pouvez cliquer sur commit.

(A noter que chaque commit que vous faites ne sera visible que par vous et présent que sur votre PC tant que vous n'avez pas push. Donc vous pouvez en faire autant que vous voulez)

<br><br>

## Mettre à jour votre branche
Avant tout, il faut commit vos changements (se référer à la section précédente)

### `git checkout develop`
(Permet de se mettre sur la branche develop)

### `git pull`
(Récupère les dernières modifications du dépot git)

### `git checkout maBranche`
(Permet de se mettre sur la branche maBranche)

### `git merge develop`
(Copie la branche de develop sur la branche courante, ici maBranche)

Après avoir exécuter toutes ces commandes, il vous suffit de régler les conflits si conflits il y a. 

<br><br>

## Comment push ces modifications ?

Avant tout, il faut mettre à jour votre branche (se référer à la section correspondante)

Une fois fais, toujours sur la branche maBranche, exécuter la commande :

### `git push`
 
Vous allez avoir une erreur lors de votre premier push sur une nouvelle branche. Copier la commande git push ... qu'on vous propose, et coller là pour l'exécuter, ça va push correctement votre code.

Ensuite, aller dans git hub, et cliquer sur le bouton "créer une pull request" puis créer votre pull request. Enfin, demander à votre mate de review la PR et les modifications avant de merge les changements afin d'avoir un deuxième avis.  


<br><br>

## Comment installer MongoDB ?

Aller sur le site:
https://www.mongodb.com/try/download/community

Créer une nouveau port de connexion : mongodb://localhost:27017/ (default port sous windows)
Run le fichier database.py package pour intialiser la database sur votre machine.
Run le fichier app.py and tout bon :)
