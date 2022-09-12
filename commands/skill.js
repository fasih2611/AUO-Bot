const { SlashCommandBuilder,EmbedBuilder,ActionRowBuilder, ButtonBuilder, ButtonStyle,CommandInteractionOptionResolver,MessageComponentInteraction, Message  } = require('discord.js');
const ServantData = require('./Data.json');

function GetServant(name){
	let len = 361;
    for(let i =1;i<=len;i++){
        if(ServantData[i]['AKA'].includes(name)){
            return ServantData[i];
        }
    }
}
function Skillformat(skill){
    let output = "";
    for(const word of skill){
        if (Array.isArray(word) && word.length >5){
            output += '\n';
            output += Skillformat(word);
            continue;
        }
        if(/\d/.test(word[0])) {output += word+" ";continue;}
        if(Array.isArray(word)){
            output += '\n';
            for(const cooldown of word){
                output += cooldown + " "
            }
            output += '\n';
            continue;
        }
        output += '\n';
        output += word
        
    }
    return output
}

module.exports = {
	data: new SlashCommandBuilder()
		.setName('skill')
		.setDescription('Gives the skills of the specified Servant!')
        .addStringOption(option=>
            option.setName('servant-name')
            .setDescription('The name of the desired servant')
            .setRequired(true)
        ),
        

	async execute(interaction) {
        if (!interaction.isChatInputCommand()) return;

		try{
			let name = interaction.options.getString('servant-name')
			Servantinfo = GetServant(name.charAt(0).toUpperCase() + name.slice(1))
			let skills = Servantinfo['skills']
			let embedarr = []
			for(let i = 1;i<=3;i++){
			
				
				const skill = new EmbedBuilder()
					.setColor(0x0099FF)
					.setTitle(Servantinfo['AKA'].substr(Servantinfo['AKA'].lastIndexOf(',')+1,Servantinfo['AKA'].length)+' Skill '+i)
					.setDescription(Skillformat(skills[i]))
					.setThumbnail(Servantinfo['art'][0]+'.png')
				embedarr.push(skill)

			}
			await interaction.reply({ embeds: embedarr});
			
			
			}
		catch{
			await interaction.reply({content:'Invalid Input'})
		}
	},
};