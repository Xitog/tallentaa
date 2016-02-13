function viewAllComposers(document, dates, months, works, authors_abc) {
    var compo_list = document.getElementById("compo_list");
    for (var i=0; i < authors_abc.length; i++) {
        var li = document.createElement('li');
        li.textContent = authors_abc[i];
        compo_list.appendChild(li);
    }
}

function viewDate(viewdate, document, dates, months, works, authors) {
    var main_list = document.getElementById("main_list");
    
    var div = document.createElement("div");
    div.setAttribute('class', 'date_nav');
    var m = viewdate.getMonth();
    var mx = { 0 : 'Janvier', 1 : 'Février', 2 : 'Mars', 3 : 'Avril', 4 : 'Mai', 5 : 'Juin', 6 : 'Juillet', 7 : 'Août', 8 : 'Septembre', 9 : 'Octobre', 10 : 'Novembre', 11 : 'Décembre'};
    
    var space = document.createElement('span');
    space.setAttribute('class', 'space_right');
    var aa = document.createElement('a');
    aa.setAttribute('class', 'button previous');
    aa.innerHTML = 'préc.';
    space.appendChild(aa);
    div.appendChild(space);
    
    space = document.createElement('span');
    aa = document.createElement('a');
    aa.setAttribute('class', 'button');
    aa.textContent = mx[m];
    space.appendChild(aa);
    div.appendChild(space);
    
    space = document.createElement('span');
    space.setAttribute('class', 'space_left');
    aa = document.createElement('a');
    aa.setAttribute('class', 'button next');
    aa.innerHTML = 'suiv.';
    space.appendChild(aa);
    div.appendChild(space);
    
    main_list.appendChild(div);
    
    for (var i = 0; i < dates.length; i++) {
        // Date
        var d = dates[i][0];
        var tab = d.split('/');
        
        var p = document.createElement("p");
        var span = document.createElement('span');
        span.setAttribute('class', 'date');
        span.textContent = tab[0];
        p.appendChild(span);

        span = document.createElement('span');
        span.setAttribute('class', 'month');
        span.textContent = months[tab[1]];
        p.appendChild(span);

        var br = document.createElement('br');
        p.appendChild(br);

        var ol = document.createElement('ol');
        for (var j = 0; j < dates[i][6].length; j++) {
            var li = document.createElement('li');
            var author = dates[i][6][j][0];
            var opus = dates[i][6][j][1];
            var opus_title = works[author][opus];
            var author_short = authors[author];

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
        main_list.appendChild(p);
        main_list.appendChild(ol);
    }
}