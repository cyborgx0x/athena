axios.post('/api/following/', {
    type: "get-follow"
}).then(array => {
    return array.data
}).then((res) => {

    for (item of res) {
        try {
            u = document.getElementById("u-" + item.affected)
            u.value = "followed"
            u.textContent = "Đã theo dõi"
        }
        catch (err) { console.log(err)}
    }

}
)
axios.get('/user/love/').then(res=>{
    for (item of res.data) {
        try {
            console.log(item)
            col = document.getElementById("col-"+item.collection_id);
            console.log(col)
            col.value = "love"
            col.style.color = "red"
        }
        catch(err) {
            console.log(err)
        }
    }
})

function addLove(context) {
    function updateLove(context, id) {
            axios.post('/user/love/', {type:"love", value:context.value, id:id}).then(
                res=>{
                    context.nextElementSibling.textContent = res.data
                })
    }
    let col_id = context.id.slice(4)
    if (context.value == "love") {
        context.value = "nolove";
        context.style.color = "rgba(255,255,255,0.8)";
        updateLove(context, col_id)
    }
    else {
        context.value = "love"
        context.style.color = "red"
        updateLove(context, col_id)
    }

}

function addFollow(context) {
    function updateFollow(context, id) {
        let data = {
            type: "user-follow",
            value: context.value,
            user: id
        }
        console.log(data)
        axios.post('/api/following/', data).then((res) => {
            console.log(res)
            context.previousSibling.previousSibling.innerHTML = res.data
        }).catch((err) => {
            context.textContent = "Đã có lỗi xảy ra"
            context.disabled = true
        })
    
    }
    let uid = context.id.slice(2)
    
    if ( context.value == "follow") {
        context.value = "followed"
        context.textContent = "Đã theo dõi"
        updateFollow(context, uid)

    } else {
        context.value = "follow"
        context.textContent = "Theo dõi"
        updateFollow(context, uid)

    }
}

