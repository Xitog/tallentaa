        
function getParameters(document) {
    var params = {};
    params.city_bdx = document.getElementById("par_city_bdx").checked;
    params.city_tlse = document.getElementById("par_city_tlse").checked;
    params.orch_onct = document.getElementById("par_orch_onct").checked;
    params.date_over = document.getElementById("par_date_over").checked;
    params.type_concert = document.getElementById("par_type_concert").checked;
    params.type_opera = document.getElementById("par_type_opera").checked;
    params.type_ballet = document.getElementById("par_type_ballet").checked;
    return params;
}

function viewAllComposers(document, dates, months, works, authors_abc) {
    var first = '';
    var compo_list = document.getElementById("compo_list");
    for (var i=0; i < authors_abc.length; i++) {
        var authors_splitted = authors_abc[i].split(' ');
        var last = authors_splitted[authors_splitted.length-1];
        if (last.charAt(0) !== first) {
            first = last.charAt(0);
            var divider = document.createElement('li');
            divider.setAttribute('class', 'divider');
            divider.textContent = first.toLocaleUpperCase();
            compo_list.appendChild(divider);
        }
        var li = document.createElement('li');
        li.textContent = authors_abc[i];
        compo_list.appendChild(li);
    }
}

function viewDate(viewdate, document, dates, months, works, authors, org_disp) {
    var main_list = document.getElementById("main_list");
    // Nettoyage
    while (main_list.firstChild) {
        main_list.removeChild(main_list.firstChild);
    }
    
    var params = getParameters(document);
    
    var div = document.createElement("div");
    div.setAttribute('class', 'date_nav');
    var m = viewdate.getMonth();
    var mx = { 0 : 'Janvier', 1 : 'Février', 2 : 'Mars', 3 : 'Avril', 4 : 'Mai', 5 : 'Juin', 6 : 'Juillet', 7 : 'Août', 8 : 'Septembre', 9 : 'Octobre', 10 : 'Novembre', 11 : 'Décembre'};
    
    var space = document.createElement('span');
    space.setAttribute('class', 'space_right');
    var aa = document.createElement('a');
    aa.setAttribute('class', 'button previous');
    aa.setAttribute('onclick', 'controlPrevDate()');
    aa.innerHTML = 'préc.';
    space.appendChild(aa);
    div.appendChild(space);
    
    space = document.createElement('span');
    aa = document.createElement('a');
    aa.setAttribute('class', 'button');
    aa.textContent = mx[m] + ' ' + String(viewdate.getFullYear()).slice(2);
    space.appendChild(aa);
    div.appendChild(space);
    
    space = document.createElement('span');
    space.setAttribute('class', 'space_left');
    aa = document.createElement('a');
    aa.setAttribute('class', 'button next');
    aa.setAttribute('onclick', 'controlNextDate()');
    aa.innerHTML = 'suiv.';
    space.appendChild(aa);
    div.appendChild(space);
    
    main_list.appendChild(div);
    
    //var mega_list = document.createElement('ul');
    //mega_list.setAttribute('class', 'list');
    //main_list.appendChild(mega_list);
    
    var nb_dates = 0;
    
    for (var i = 0; i < dates.length; i++) {
        // Check Ville
        var city = dates[i][7];
        if (!params.city_tlse && city === 'Toulouse') {
            continue;
        }
        // Check Date Over
        var d = dates[i][0];
        var tab = d.split('/');
        if (!params.date_over) {
            var dNow = new Date();
            var dDate = Date.parse(tab[1] + '/' + tab[0] + '/' + tab[2]);
            if (dDate < dNow) {
                continue;
            }
        }
        // Check Orchestra
        if (!params.orch_onct && dates[i][2] === 'ONCT') {
            continue;
        }
        // Check Type
        if (!params.type_concert && dates[i][9] == 'Concert') {
            continue;
        }
        if (!params.type_opera && dates[i][9] == 'Opéra') {
            continue;
        }
        if (!params.type_ballet && dates[i][9] == 'Ballet') {
            continue;
        }
        // Check Date for Month
        if (parseInt(tab[1]) !== (viewdate.getMonth() + 1)) {
            continue;
        }
        // If all is good
        nb_dates++;
        
        //var mega_li = document.createElement('li');
        var mega_div = document.createElement('div');
        mega_div.setAttribute('class', 'date_elem');
        
        var p = document.createElement("p");
        var span = document.createElement('span');
        span.setAttribute('class', 'date');
        span.textContent = tab[0];
        p.appendChild(span);

        span = document.createElement('span');
        span.setAttribute('class', 'month');
        span.textContent = months[tab[1]];
        p.appendChild(span);
        
        span = document.createElement('span');
        span.setAttribute('class', 'space_left icon clock mini');
        span.textContent = dates[i][1];
        p.appendChild(span);
        span = document.createElement('span');
        span.setAttribute('class', 'space_left icon home mini');
        span.textContent = dates[i][8];
        p.appendChild(span);
        
        var p2 = document.createElement("p");
        span = document.createElement('span');
        span.textContent = dates[i][9];
        p2.appendChild(span);
        span = document.createElement('span');
        span.setAttribute('class', 'space_left icon star');
        span.textContent = org_disp[dates[i][2]];
        p2.appendChild(span);
        
        var br = document.createElement('br');
        p.appendChild(br);
        
        var ol = document.createElement('ol');
        ol.setAttribute('class', 'custom-counter');
        for (var j = 0; j < dates[i][6].length; j++) {
            var li = document.createElement('li');
            if (dates[i][9] == 'Concert' || (dates[i][9] == 'Ballet' && dates[i][6].length > 1)) { // Pour les ballets avec différentes pièces
                li.setAttribute('class', 'x');
            }
            
            var author = dates[i][6][j][0];
            var opus = dates[i][6][j][1];
            var opus_title = works[author][opus];
            var author_short = authors[author];

            if (dates[i][6][j].length === 3) { // Pour les ballets sur une musique de 
                span = document.createElement('span');
                span.textContent =  dates[i][6][j][2] + ' sur la musique de ';
                li.appendChild(span);
            }
            
            span = document.createElement('span');
            span.setAttribute('class', 'author');
            span.textContent = author_short;
            li.appendChild(span);
            
            span = document.createElement('span');
            span.textContent = ' : ' + opus_title;
            li.appendChild(span);

            //li.appendChild(document.createTextNode(author_short + ' : ' + opus_title));
            ol.appendChild(li);
            //span = document.createElement('span');
            //span.textContent = author_short + ' : ' + opus_title;
        }
        
        //main_list.appendChild(p);
        //main_list.appendChild(p2);
        //main_list.appendChild(ol);
        
        //mega_li.appendChild(p);
        //mega_li.appendChild(p2);
        //mega_li.appendChild(ol);
        //mega_list.appendChild(mega_li);
        
        mega_div.appendChild(p);
        mega_div.appendChild(p2);
        mega_div.appendChild(ol);
        main_list.appendChild(mega_div);
    }
    
    if (nb_dates === 0) {
        var nothing = document.createElement('span');
        nothing.textContent = 'Pas de concerts ce mois-ci.';
        main_list.appendChild(nothing);
    }
}