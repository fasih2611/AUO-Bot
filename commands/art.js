const { SlashCommandBuilder, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle, CommandInteractionOptionResolver, MessageComponentInteraction, Message } = require('discord.js');
const ServantData = require('./Data.json');

function GetServant(name) {
  let len = 361;
  for (let i = 1; i <= len; i++) {
    if (ServantData[i]['AKA'].includes(name)) {
      return ServantData[i]
    }
  }
}


module.exports = {
  data: new SlashCommandBuilder()
    .setName('art')
    .setDescription('Gives the Ascension art for specified servant!')
    .addStringOption(option =>
      option.setName('servant-name')
        .setDescription('The name of the desired servant')
        .setRequired(true)
    ),


  async execute(interaction) {
    if (!interaction.isChatInputCommand() && !interaction.isButton()) return;

    try {
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
      Servantinfo = GetServant(name.charAt(0).toUpperCase() + name.slice(1))
      art = Servantinfo['art']
      const embed = new EmbedBuilder()
        .addFields({ name: 'Traits', value: Servantinfo['Traits'], inline: true })
        .setColor(0x0099FF)
        .setTitle(Servantinfo['AKA'].substr(Servantinfo['AKA'].lastIndexOf(',') + 1, Servantinfo['AKA'].length))
        .setImage(art[art_index] + '.png')
        .setDescription('Voice Actor: ' + Servantinfo['Voice Actor'] + '\n' + 'Illustrator: ' + Servantinfo['Illustrator'] +
          '\n' + 'Alignments: ' + Servantinfo['Alignments'])
        .setFooter({ text: 'Id: ' + Servantinfo['ID'] })


      await interaction.reply({ embeds: [embed], components: [row] });

      const filter = i => (i.customId === 'forward' || i.customId === 'backward') && i.user.id === interaction.user.id;

      const collector = interaction.channel.createMessageComponentCollector({ filter, time: 15000, max: "30" });

      collector.on('collect', async i => {

        if (i.customId == 'forward') ++art_index;
        if (i.customId == 'backward') --art_index;
        if (art.length - 1 < art_index) art_index = 0;
        if (art_index < 0) art_index = art.length - 1;

        const new_embed = new EmbedBuilder()
          .setColor(0x0099FF)
          .setTitle(Servantinfo['AKA'].substr(Servantinfo['AKA'].lastIndexOf(',') + 1, Servantinfo['AKA'].length))
          .setImage(art[art_index] + '.jpg')
          .addFields({ name: 'Traits', value: Servantinfo['Traits'], inline: true })
          .setDescription('Voice Actor: ' + Servantinfo['Voice Actor'] + '\n' + 'Illustrator: ' + Servantinfo['Illustrator'] +
            '\n' + 'Alignments: ' + Servantinfo['Alignments'])
          .setFooter({ text: 'Id: ' + Servantinfo['ID'] });

        await i.update({ embeds: [new_embed] })
      });
      collector.on("end", async () => {
        await interaction.editReply({ components: [] })
      });
    }
    catch {
      await interaction.reply({ content: 'Invalid Input' })
    }
  },
};