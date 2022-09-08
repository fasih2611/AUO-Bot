const { SlashCommandBuilder,EmbedBuilder,ActionRowBuilder, ButtonBuilder, ButtonStyle,CommandInteractionOptionResolver,MessageComponentInteraction  } = require('discord.js');
const ServantData = require('./Data.json');

function GetServantArt(name){
	let len = 361;
    for(let i =1;i<len;i++){
        if(ServantData[i]['AKA'].includes(name)){
            return ServantData[i]
        }
    }
}


module.exports = {
	data: new SlashCommandBuilder()
		.setName('art')
		.setDescription('Gives the ascension art for a specified servant!')
        .addStringOption(option=>
            option.setName('servant-name')
            .setDescription('The name of the desired servant')
            .setRequired(true)
        ),
        

	async execute(interaction) {
        if (!interaction.isChatInputCommand()) return;
		try{
			if (interaction.isButton()){
				console.log('pog');
				return
			}
		
			var art_index = 0
			const row = new ActionRowBuilder()
				.addComponents(
					new ButtonBuilder()
						.setCustomId('backward')
						.setLabel('⬅')
						.setStyle(ButtonStyle.Primary),
					new ButtonBuilder()
					.setCustomId('forward')
					.setLabel('➡')
					.setStyle(ButtonStyle.Primary)
				);
				let name = interaction.options.getString('servant-name')
				Servantinfo = GetServantArt(name.charAt(0).toUpperCase() + name.slice(1))
				art = Servantinfo['art']
				const embed = new EmbedBuilder()
				.setColor(0x0099FF)
				.setTitle(Servantinfo['AKA'].substr(Servantinfo['AKA'].lastIndexOf(',')+1,Servantinfo['AKA'].length))
				.setImage(art[art_index]+'.jpg')
				.setDescription('Voice Actor: '+Servantinfo['Voice Actor']+'\n'+'Illustrator: '+Servantinfo['Illustrator']+
				'\n'+'Alignments: '+Servantinfo['Alignments'])
				.setFooter({ text: 'Id: '+Servantinfo['ID']})
				
				
			await interaction.reply({ embeds: [embed], components: [row] });
			
				// if(interaction)

				// if(art.length-1<art_index) art_index=0
				// if(art_index<0) art_index=art.length-1
				
				// const new_embed = new EmbedBuilder()
				// .setColor(0x0099FF)
				// .setTitle(Servantinfo['AKA'].substr(Servantinfo['AKA'].lastIndexOf(',')+1,Servantinfo['AKA'].length))
				// .setImage(art[art_index]+'.jpg')
				// .setDescription('Voice Actor: '+Servantinfo['Voice Actor']+'\n'+'Illustrator: '+Servantinfo['Illustrator']+
				// '\n'+'Alignments: '+Servantinfo['Alignments'])
				// .setFooter({ text: 'Id: '+Servantinfo['ID']});
				// interaction.update({embeds: [new_embed]})
			}
		catch{
			await interaction.reply({content:'Invalid Input'})
		}
	},

};