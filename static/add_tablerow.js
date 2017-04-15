function deleteRow(row, varVal)
{
    console.log('double hello');
    console.log(varVal)
    var i=row.parentNode.parentNode.rowIndex;
    document.getElementById('POITable'+varVal).deleteRow(i);
}


function insRow(varVal)
{
    console.log( 'hi');
    console.log(varVal)
    var x=document.getElementById('POITable'+varVal);
    var new_row = x.rows[1].cloneNode(true);
    var len = x.rows.length;
    new_row.cells[0].innerHTML = len;
    
    var inp1 = new_row.cells[1].getElementsByTagName('input')[0];
    inp1.id += len;
    inp1.value = '';
    var inp2 = new_row.cells[2].getElementsByTagName('select')[0];
    inp2.id += len;
    inp2.value = '';
    x.appendChild( new_row );
}