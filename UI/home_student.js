var tt = {
    "0":{
        "1":"Physics",
        "2":"sadf",
        "3":"Free"
    },
    "1":{
        "1":"asdfsad",
    }
}
var myTab = document.getElementById("timeTable");
for (i = 0; i < myTab.rows.length; i++) {

    var objCells = myTab.rows.item(i).cells;
    for (var j = 1; j < objCells.length; j++) {
        
         objCells.item(j).children[0].innerHTML=tt[i][j];
    }
  
}