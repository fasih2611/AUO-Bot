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
function Npformat(np){
    output = "";
    output += `${np.rank}\n**${np.Hits}**\n\n`
    for(const word of np['Scaling']){
        if(/\d/.test(word[0])) {output += word+" ";continue;}
		output += `*${word}*`
        output +='\n'
    }
	output +='\n'
	for(const word of np['Effect']){
		if(/\d/.test(word[0])) {output += word+" ";continue;}
		output += `*${word}*`
        output +='\n'
	}
	for(const word of np['Overcharge Effect']){
		if(/\d/.test(word[0])) {output += word+" ";continue;}
		output +='\n'
		output += `*${word}*`
        output +='\n'
	}
	if(np.hasOwnProperty('Upgrade')){
		const upgradetext = Npformat(np.Upgrade).output
		return {upgradetext,output}
	}
	return {output};
}
module.exports = {
	data: new SlashCommandBuilder()
		.setName('np')
		.setDescription('Gives the Noble Phantasm of the specified Servant!')
        .addStringOption(option=>
            option.setName('servant-name')
            .setDescription('The name of the desired servant')
            .setRequired(true)
        ),
	async execute(interaction) {
        if (!interaction.isChatInputCommand()) return;

		try{
			let name = interaction.options.getString('servant-name');
			Servantinfo = GetServant(name.charAt(0).toUpperCase() + name.slice(1));
			let np = Servantinfo['NP'];
			text = Npformat(np);
			const embed = new EmbedBuilder()
					.setColor(0x0099FF)
					.setTitle(np['name'])
					.setDescription(`**${np['ftext']}**\n${text.output}`)
					.setThumbnail(Servantinfo['art'][0]+'.png')
					.addFields({name:'Type',value:np['type'],inline:true})

			if(text.hasOwnProperty('upgradetext')){
				const embed2 = new EmbedBuilder()
					.setColor(0x0099FF)
					.setTitle('Upgrades To:')
					.setDescription(text.upgradetext)
				await interaction.reply({ embeds: [embed,embed2]});
				return;	
			}
			await interaction.reply({ embeds: [embed]});
			}
		catch(err){
			console.log(err);
			await interaction.reply({content:'Invalid Input'});
		}
	},
};