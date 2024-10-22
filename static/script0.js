try{
  const text = document.querySelector(".span1");

const load = () => {
     setTimeout(() =>{
      text.textContent = "Your Little Krishna: Here to Save Your File!";
    },0);
    setTimeout(() =>{
        text.textContent = "Giving Back What You Gave!";
      },5000);
  
}

setInterval(load, 5000);
}
catch(e){
  console.log('span1 not found')
}
