$(document).ready(function() {
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});
document.addEventListener("DOMContentLoaded", function(){
    let vinRadio = document.querySelector('#inlineRadio1')
    let gosRadio = document.querySelector('#inlineRadio2')
    let inputForm = document.querySelector('#entervalue')
    document.querySelector('#inlineRadio2').name='reject'
    document.querySelector('#inlineRadio1').name='select'

    let onVinInput = function(e){
//    console.log('vin selected?', vinRadio.checked)
//    console.log('gos selected?', gosRadio.checked)
    inputForm.placeholder = '1ABCD12345EF26789'
    document.querySelector('#inlineRadio2').name='reject'
    document.querySelector('#inlineRadio1').name='select'
    vinRadio.checked=true
    gosRadio.checked=false
    };

    let onGosInput = function(e){
//    console.log('vin selected?', vinRadio.checked)
//    console.log('gos selected?', gosRadio.checked)
    inputForm.placeholder = 'А123АА123'
    document.querySelector('#inlineRadio1').name='reject'
    document.querySelector('#inlineRadio2').name='select'
    gosRadio.checked=true
    vinRadio.checked=false
    };
    let onInput = function(e){
        let input = e.target

        document.querySelector('#entervalue').value = input.value
    }

    vinRadio.addEventListener("input", onVinInput);
    gosRadio.addEventListener("input", onGosInput);
    inputForm.addEventListener("input", onInput);
    });
