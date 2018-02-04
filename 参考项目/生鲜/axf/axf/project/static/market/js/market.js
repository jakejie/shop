$(document).ready(function(){
    var alltypebtn=document.getElementById('alltypebtn')
    var showsortbtn=document.getElementById('showsortbtn')

    var typediv=document.getElementById('typediv')
    var sortdiv=document.getElementById('sortdiv')

    typediv.style.display='none'
    sortdiv.style.display='none'

    alltypebtn.addEventListener('click',function(){
        typediv.style.display='block'
        sortdiv.style.display='none'
    },false)
    showsortbtn.addEventListener("click", function(){
        typediv.style.display = "none"
        sortdiv.style.display = "block"
    },false)
    typediv.addEventListener("click", function(){
        typediv.style.display = "none"
    },false)
    sortdiv.addEventListener("click", function(){
        sortdiv.style.display = "none"
    },false)

    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/0/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                } else {
                    if (data.data == -1){
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        })
    }


    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function(){
            pid = this.getAttribute("ga")
            $.post("/changecart/1/",{"productid":pid}, function(data){
                if (data.status == "success"){
                    //添加成功，把中间的span的innerHTML变成当前的数量
                    document.getElementById(pid).innerHTML = data.data
                } else {
                    if (data.data == -1){
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        })
    }

})





