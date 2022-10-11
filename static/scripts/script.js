///* static/script.js */
//const btnDelete= document.querySelectorAll('.btn-delete');
//if(btnDelete) {
//  const btnArray = Array.from(btnDelete);
//  btnArray.forEach((btn) => {
//    btn.addEventListener('click', (e) => {
//      if(!confirm('Esti sigur ca vrei sa stergi?')){
//        e.preventDefault();
//      }
//    });
//  })
//}
//
//
//var numeError = document.getElementById('nume-error');
//var prenumeError = document.getElementById('prenume-error');
//var marcaError = document.getElementById('marca-error');
//var submitError = document.getElementById('submit-error');
//
//function validateNume(){
//    var nume = document.getElementById("contact-nume").value;
//
//    if(nume.length == 0){
//        numeError.innerHTML = 'Completeaza numele';
//        return false;
//    }
//    if(!nume.match(/^[A-Z]*$/)){
//        numeError.innerHTML = 'Numele incorect';
//        return false;
//    }
//    numeError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
//    return true;
//}
//
//function validatePrenume(){
//     var prenume = document.getElementById("contact-prenume").value;
//
//    if(prenume.length == 0){
//        prenumeError.innerHTML = 'Completeaza prenumele';
//        return false;
//    }
//    if(!prenume.match(/^[A-Z]*$/)){
//        prenumeError.innerHTML = 'Prenumele incorect';
//        return false;
//    }
//    prenumeError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
//    return true;
//}
//
//function validateMarca(){
//     var trs_id = document.getElementById("contact-trs_id").value;
//
//    if(trs_id.length == 0){
//        trs_idError.innerHTML = 'Completeaza  nr. marca';
//        return false;
//    }
//    if(!trs_id.match(/^[0-9]*$/)){
//        trs_idError.innerHTML = 'Nr.marca incorect';
//        return false;
//    }
//    trs_idError.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
//    return true;
//}
//
//function validateForm(){
//    if(!validateNume() || !validatePrenume() || !validateMarca()){
//        submirError.innerHTML = 'exista o eroare';
//        return false;
//    }
//}
//
