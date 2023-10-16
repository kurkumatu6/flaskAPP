async function postJSON(route, data){
    let response = await fetch(route, {
        method: "POST",
        headers: {
          "Content-Type": "application/json;charset=UTF-8", //обязательный заголовок для формата json
        },
        body: JSON.stringify(data),
      });
      return await response.json()
}

document.querySelectorAll(".linkType").forEach(item => {
    item.addEventListener("change", function(e){
        postJSON('/changeLinkType', {id: e.currentTarget.dataset.id, type: e.currentTarget.value})
    })
})
document.addEventListener("change", function(e){
    if(e.target.classList.contains("linkType")){
        postJSON('/changeLinkType', {id: e.target.dataset.id, type: e.target.value})
    }
})
document.addEventListener('click', function(e){
    if(e.target.classList.contains("delLink")){
        postJSON("/getLinkName", {id: e.target.dataset.id}).then(function(nicname){
            postJSON("/gethostname", '').then(function(hostName){
                document.querySelector("body").insertAdjacentHTML("beforeend", `
                <div class="modal-wrapper">
                    <div class="modal ShowRewiewModal">
                        <button id="closeModal">x</button>
                        <div>
                            <h2>${hostName}${nicname}</h2>
                            <button class="delLinkConfirm" data-id='${e.target.dataset.id}'>Подтвердить удаление</button>
                        </div>
                    </div>
                  </div>
                `)
                modal = document.querySelector(".modal-wrapper")
                    document.querySelector(".delLinkConfirm").addEventListener("click", function(event){
                        let id = event.currentTarget.dataset.id
        
        
                            postJSON('/delLink', {id: id}).then(function(value){
                                let table = document.querySelector("#linksTable")
                                table.innerHTML = `            
                                <tr>
                                <td>Ссылка</td>
                                <td>Псевдоним</td>
                                <td></td>
                                <td>Тип ссылки</td>
                                <td></td>
                                </tr>`;
                                value.forEach(item => {
                                    table.insertAdjacentHTML("beforeend",`
                                    <tr>
                                    <td>${item[1]}</td>
                                    <td>${hostName}${item[2]}</td>
                                    <td></td>
                                    <td><select name="" class="linkType" id="linkType${item[0]}" data-id="${item[0]}">
                                    </select></td>
                                    <td><button class="delLink" data-id="${item[0]}">Удалить</button>
                                    <button class="changeLink" data-id="${item[0]}">Изменить псевдоним</button></td>
                                    </tr>
                                    `)
                                    postJSON('/getlinkTypes', '').then(function(value){
                                        let select = document.querySelector(`#linkType${item[0]}`)
                                        value.forEach(type =>{
                                            select.insertAdjacentHTML('beforeend', `
                                                <option value="${type[0]}"  ${item[4] == type[0] ? "selected": "" }>${type[1]}</option>
                                            `)
                                        })
                                    })
                                })
                            })
        
                        modal.remove()
                    })
        
                modal.addEventListener("click", function(e){
                  if(e.target == e.currentTarget){
                    modal.remove()
                  }
                })
                document.addEventListener("keyup", function(e){
                  console.log(e.key)
                  if(e.key == "Escape"){
                    modal.remove()
                  }
                })
                document.querySelector('#closeModal').addEventListener("click", function(e){
                    modal.remove()
                })
            })
        })
       
    }

    if(e.target.classList.contains("changeLink")){
        postJSON("/getLinkName", {id: e.target.dataset.id}).then(function(nicname){
            postJSON("/gethostname", '').then(function(hostName){
                document.querySelector("body").insertAdjacentHTML("beforeend", `
                <div class="modal-wrapper">
                    <div class="modal ShowRewiewModal">
                        <button id="closeModal">x</button>
                        <div>
                        <form action="/changeLinkNickName" method="post">
        

                            <h2>Изменить псевдоним</h2>
                            <label for="nickName">${hostName}</label>
                            <input type="text" name="nickName" value=${nicname}>
                            <button class="changeLinkConfirm" name="id" value='${e.target.dataset.id}'>Подтвердить изменение</button>
                            <button class="changeLinkConfirm" name="random" value='${e.target.dataset.id}'>Случайный псевдоним</button>
                        </form>
                        </div>
                    </div>
                  </div>
                `)
                modal = document.querySelector(".modal-wrapper")
                modal.addEventListener("click", function(e){
                    if(e.target == e.currentTarget){
                      modal.remove()
                    }
                  })
                  document.addEventListener("keyup", function(e){
                    console.log(e.key)
                    if(e.key == "Escape"){
                      modal.remove()
                    }
                  })
                  document.querySelector('#closeModal').addEventListener("click", function(e){
                      modal.remove()
                  })
            })
        })
    }
})

