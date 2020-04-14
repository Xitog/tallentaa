!doctrine ADD_CSS=https://xitog.github.io/dgx/css/palatino.css

# Marklight

Ce document décrit le langage **marklight**. Comme [Markdown] ou [Textile], c'est un [langage de balisage léger] pour écrire de la documentation dans un fichier texte, directement lisible sans transformation, mais pouvant également être transformé en HTML.

On peut faire des commentaires en commençant une ligne par \-\-.

-- Ceci est un commentaire il ne sera pas exporté

!doctrine EXPORT_COMMENT=true

-- Ceci est un commentaire il sera exporté en HTML

## Modification de texte

* \*\***gras**\*\* : pour mettre en gras
* \'\'''italique''\'\' : pour mettre en italique
* \-\---barré--\-\- : pour barré
* \_\___souligné__\_\_ : pour souligner
* \^\^^^exposant^^\^\^ : pour mettre en exposant

## Listes

* \* une liste non numérotée

- \- une autre liste non numérotée

% \% une liste numérotée

## Tables

* Un tableau s'écrit ainsi : |col1|col2|col3|
* La ligne de titre doit être la première et séparée par des colonnes |\-\-\-\-|

|Ceci|est|un  |tableau    |
|----|---|----|-----------|
|Il  |est|beau|mon tableau|

## Liens

* à mettre

## Doctrines

On peut utiliser !doctrine en début de ligne pour modifier des variables globales de transformation en HTML. Par exemple :

* !doctrine EXPORT_COMMENT = true/false spécifie si les commentaires seront exportés en HTML ou pas
* !doctrine ADD_CSS=lien vers un fichier CSS spécifie un fichier CSS à ajouter

[Markdown]: https://en.wikipedia.org/wiki/Markdown
[Textile]: https://en.wikipedia.org/wiki/Textile_(markup_language)
[langage de balisage léger]: https://en.wikipedia.org/wiki/Lightweight_markup_language
