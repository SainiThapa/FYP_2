console.log("loaded js")
var seeMoreButtons=document.querySelectorAll('.seemoreButton');
seeMoreButtons.forEach(button=>{
    button.addEventListener('click',function(){

        var card=this.closest('.lawyer-card');
        var content=card.querySelector('.card-content-hidden')

        if (content.style.display === 'none' || content.style.display=="") {
            content.style.display = 'block';
            this.textContent = 'Hide Computation';
        } else {
            content.style.display = 'none';
            this.textContent = 'View Computation';
        }
    });
});

// function toggleCardHeight(cardId) {
//     let card = document.getElementById(cardId);
//     console.log(card)
//     if(card.style.height=="auto"){
//         card.style.height ='600px';
//     }
//     else{
//         card.style.height='auto';
//     }
// }