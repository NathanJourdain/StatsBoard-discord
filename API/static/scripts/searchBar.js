const searchBarInput = document.querySelector('.search-bar input');
const searchBarContainer = document.querySelector('.search-bar .container');

if(searchBarInput != undefined){

    searchBarInput.addEventListener('input', (e) => {
        searchBarContainer.innerHTML = '';
        userGuilds.forEach(guild => {
            if(guild.guild_name.toLowerCase().startsWith(e.target.value.toLowerCase())){
                searchBarContainer.appendChild(createSearchBarItem(guild));
            }
        })
    });
}

const createSearchBarItem = (guild) => {
    const item = document.createElement('a');
    item.href = `/guilds/${guild.guild_id}`;
    item.innerText = guild.guild_name;
    return item;
}