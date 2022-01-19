# PLAN ORAL

## Accroche :

Salut Alex,
Merci de m'avoir accordé cette réunion. Je vais pouvoir te présenter mon travail sur SoftDesk et écouter tes remarques à ce sujet.

## Objectifs du projet :

Avant de commencer, j'aimerais brièvement rappeler quels étaient les objectifs du projet.

Tu m'as chargé de développer une application d'issue tracking fonctionnant sur différentes plateformes comme iOS ou Android. Cette application doit permettre notamment de créer des projets, d'ajouter et supprimer des contributeurs à ce projet. De créer des problèmes liés au projet et des commentaires liés au problème eux-mêmes liés aux projets.

Pour ce faire, tu as choisi de partir sur une API RESTful pour standardiser le traitement des données. Et c'est le framework Django REST qui a été choisi pour le développement.

Pour aider à la compréhension du fonctionnement de l'API, il fallait aussi rédiger une documentation.

Et enfin, je devais respecter une liste de vérification OWASP qui se situe dans un document Word que tu m'as envoyé.

## Méthode :

Pour arriver au résultat que je vais te montrer voici la méthode que j'ai utilisée.

Tout d'abord, j'ai pris le temps de bien comprendre le brief et lire les documents et d'écrire ma définition of done de l'application.

Puis j'ai créé l'architecture que je pensais la plus adaptée pour le projet. En séparant l'authentification de la partie projet pour plus faciliter l'implémentation de futur features.

J'ai ensuite installé mon environnement virtuel et commencé le développement de la partie authentification en implémentant la fonctionnalité de JWT comme demandée dans le brief.

Une fois les modèles, vues, serializers et urls implémentés, J'ai effectué une série de tests pour voir si mon authentification fonctionnait notamment sur la durée du token, la réattribution de token, l'accès au endpoints dans le projet (j'avais implémenté l'endpoint GET projet pour le test)

Une fois l'authentification fonctionnelle, j'ai implémenté la partie projet.

Pour la partie projet, j'ai commencé à écrire les modèles pour les projets, les problèmes, les commentaires, les contributeurs.
Puis j'ai travaillé sur les serializers et les vues et enfin j'ai implémenté les urls.

Une fois toutes la partie projet fonctionnelle et la première version de la documentation écrite (test réalisé sur tous les endpoints), je suis passé à l'écriture des permissions pour chacun des endpoints. 

Et enfin j'ai effectué un bref refactoring de mes méthodes pour que le code soit plus lisible.

Durant tous le long du développement, j'ai respecté PEP8 et les conventions de nommages de mes méthodes.

Enfin j'ai refais une passe sur toute la documentation pour la corriger et la rendre plus lisible pour les utilisateurs de l'API et j'ai implémenté les fonctionnalités liées à la RGPD

## Présentation des endpoints : 

Le nombre total d'endpoint de l'API s'élève à : 19.
Il existe deux endpoints liés à l'authentification et le reste concerne les projets.

Chaque endpoint respecte la définition demandée dans le brief. 

## OWASP & RGPD

Pour ce qui est de OWASP, j'ai respecté les directives données dans le document Word à savoir :

- l'utilisation d'un token JWT pour l'authentification.
- l'autorisation d'accès à l'API si l'utilisateur est authentifié (possède un token). Pour chaque endpoint je vérifie si il possède le token.
- les règles de permissions pour chaque endpoint (un utilisateur n'est pas autorisé à un projet si il n'est pas un contributeur par exemple)

En ce qui concerne le top 10 des vulnérabilités OWASP, DRF a des fonctionnalités built in pour les gérer. 

### A1 = Injection
Par exemple prenons le cas des attaques par injections SQL. Et bien DRF a un ORM par défaut qui protège l'API. Par exemple dans le cas de la classe de la variable Password et et bien je fais appel à models.PasswordField qui définit le comportement des champs password en limitant les caractères autorisés.

### A2 = Broken Authentication
Par ailleurs, j'ai implémenté une Django Rate Limit pour limiter le nombre de requêtes que l'utilisateur peut effectuer sur le endpoint d'authentification.
Je n'ai pas incorporé de fonctionnalité de double authentification mais je sais que je peux l'implémenter facilement si besoin est.

### A3 = Sensitive Data Exposure
Sensitive data like passwords are never stored in plain text. Ils sont convertis en hash avant d'être stockés dans la base de données. 
Par ailleurs le site étant dev en local, il n'y a pas besoin d'encrypté les requêtes pour le moment.

### A4 = XML External Entities (XXE)
Sur Django rest Framework il est difficle de réaliser ce genre d'ataque car DRF sérialize et désérialize les données à chaque manipulation.

### A5 = Broken Access Control
Pour empêcher ça je demande le token de l'utilisateur dans chaque endpoint et en plus de ce token, j'ai écris un fichier de permission qui s'occupe de vérifier si l'utilisateur est autorisé à accéder à certaines requêtes de l'endpoint.

### A6 = Security Misconfiguration
Il y a certaines choses auquel il faut faire attention lorsqu'on passe en production. 
Notamment mettre le mode debug sur False.
