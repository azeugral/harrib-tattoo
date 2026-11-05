# -*- coding: utf-8 -*-
"""Conteúdo real do Alisson: tudo aqui saiu do Instagram dele (legendas, comentários e stories)."""

# id, título, série/nota, categorias, arquivo da capa, foco y do recorte 4:5, mídias extras, fala dele na legenda
TRABALHOS = [
    ('chrollo', 'Chrollo', 'Hunter × Hunter', ['manga'], '002_0', .46, ['002_1', '002_2'], 'A primeira de HxH. Estou bem feliz com esse resultado!'),
    ('vermelha', 'Anime em traço vermelho', 'Composição de mangá', ['manga', 'cor'], '001_0', .42, ['001_1'], 'Eu adoro fazer esses projetos de anime/mangá, e a composição desse ficou demais!'),
    ('uzumaki', 'Uzumaki', 'Junji Ito', ['manga'], '011_0', .40, ['011_1'], 'Mais uma de Junji Ito, esse trabalho foi bem satisfatório de fazer e eu amo esse estilo mangá.'),
    ('besouro', 'Besouro', 'Blackwork', ['black'], '003_0', .46, ['003_1'], 'Que fusão insana!!'),
    ('gohan', 'Gohan', 'Saga Cell, Dragon Ball', ['manga'], '010_0', .50, ['010_1'], 'Fazer tatuagens no estilo mangá/anime está sendo uma experiência muito boa, dessa vez um Gohan da saga Cell.'),
    ('caveira', 'Caveira cybertribal', 'Ombro e braço', ['cyber'], '006_1', .46, ['006_0'], 'Extremamente satisfeito com esse resultado.'),
    ('tomie', 'Tomie', 'Junji Ito', ['manga'], '013_0', .50, [], 'Tomie de Junji Ito, eu sempre quis tatuar essa arte!'),
    ('lirio', 'Lírio em preto e vermelho', 'Ombro', ['floral', 'black'], '015_1', .50, ['015_0', '015_2'], 'Que tattoo boa de fazer! A sessão foi ótima e a arte me agradou muito.'),
    ('hannya', 'Hannya', 'Blackwork', ['black'], '018_1', .50, ['018_0'], 'A evolução para no momento em que meu esforço para.'),
    ('soul', 'Sol e lua', 'Soul Eater', ['manga'], '009_1', .48, ['009_0'], 'Essa tattoo foi premiação na Batalha da Meno.'),
    ('perna', 'Perna cybertribal', 'Coxa ao tornozelo', ['cyber'], '017_1', .42, ['017_0', '017_2'], 'Foi um trabalho de muitas horas mas que valeu cada minuto.'),
    ('capuz', 'Figura de capuz', 'Inspirada em Bring Me The Horizon', ['black'], '019_0', .46, ['019_1'], 'Tattoo inspirada em Bring Me The Horizon.'),
    ('caveiraflor', 'Caveira e flores', 'Coxa', ['floral'], '014_1', .50, ['014_0'], 'A arte é linda e todo o tempo dedicado nela valeu cada segundo.'),
    ('zoro', 'Zoro', 'One Piece', ['manga'], '034_1', .46, ['034_0'], 'Fine art do Zoro.'),
    ('freehand', 'Primeiro freehand', 'Antebraço', ['cyber'], '024_1', .50, ['024_0', '024_2'], 'Saber que é exclusiva tanto pra mim quanto pro meu cliente é uma sensação indescritível!'),
    ('mao', 'Mão cybertribal', 'Projeto em andamento', ['cyber'], '007_0', .50, [], 'Apesar de não estar pronto, está sendo um dos projetos mais bonitos que já fiz. Postei porque sou ansioso kkkkkk'),
    ('lirios', 'Lírios', 'Floral em traço fino', ['floral'], '012_0', .50, ['012_1'], 'Estou adorando fazer o estilo floral, além de ser muito elegante, é uma ótima forma de desenvolver melhor meu traço.'),
    ('cordeiro', 'Cordeiro', 'Cult of the Lamb', ['cor', 'manga'], '020_0', .50, ['020_2', '020_1'], 'Trabalhar com um pouco de cor além do preto é muito bom também, e é uma das minhas favoritas agora.'),
    ('autoral', 'Arte autoral', 'Lembrança eternizada', ['cyber'], '016_1', .50, ['016_0'], 'Essa tattoo é muito especial pra mim, tanto por ser uma arte autoral quanto pelo contexto da criação dela.'),
    ('quatro', 'Filigrana em 4 cores', 'Antebraço', ['cor', 'floral'], '008_0', .50, ['008_1', '008_2'], 'Adorei essa tattoo, trabalhei com 4 cores e ela é bem delicada.'),
    ('bobo', 'Bobo da corte', 'Primeira vez com agulha RS', ['black'], '022_0', .46, ['022_1'], 'Foi um projeto de última hora mas foi incrível de se fazer!'),
    ('dragao', 'Dragão', 'Primeira tattoo detalhada', ['black'], '029_0', .42, [], 'Foram horas de trabalho e valeu cada segundo.'),
    ('esqueleto', 'Mão de esqueleto', 'Avenged Sevenfold', ['floral'], '032_0', .36, [], 'Tatuagens com traços delicados e finos é algo que eu quero fazer muito mais vezes.'),
    ('capivara', 'Capivara', 'Vermelho e preto', ['cor'], '033_0', .40, ['033_1', '033_2'], 'Tatuagens assim dão um charme muito legal.'),
    ('alquimia', 'Círculo de transmutação', 'Fullmetal', ['manga', 'cor'], '027_0', .40, [], 'Tattoo inspirada em Fullmetal.'),
]

FILTROS = [('todos', 'Tudo'), ('manga', 'Mangá e anime'), ('cyber', 'Cybertribal'), ('floral', 'Floral e traço fino'), ('black', 'Blackwork'), ('cor', 'Com cor')]

# Arco: da direita para a esquerda, como se lê mangá
ARCO = [
    ('abr', 'Abril', 'Workshop com a Dehar', 'Já saio do dia 1 com outro olhar sobre o meu próprio traço!', '039_0_q', 'workshop'),
    ('auto', 'Abril', 'Auto tattoo', 'Uma das melhores formas de evoluir é sentir na própria pele cada detalhe do processo.', '036_0', 'auto'),
    ('detalhe', 'Maio', 'Primeira detalhada', 'Foram horas de trabalho e valeu cada segundo.', '029_0', 'dragao'),
    ('esforco', 'Maio', 'A regra', 'A evolução para no momento em que meu esforço para.', '018_1', 'hannya'),
    ('freehand', 'Junho', 'Primeiro freehand', 'É uma sensação indescritível.', '024_1', 'freehand'),
    ('ito', 'Agosto', 'Junji Ito', 'Eu amo esse estilo mangá, espero que apareça mais pessoas buscando fazer!', '011_1', 'uzumaki'),
    ('meno', 'Setembro', 'Premiação', 'Tattoo de prêmio na Batalha da Meno.', '009_1', 'soul'),
    ('hxh', 'Outubro', 'Chrollo', 'A primeira de HxH. Estou bem feliz com esse resultado!', '002_1', 'chrollo'),
]

# Comentários e mensagens reais de clientes e colegas
FALAS = [
    ('Tu é muito foda, eu amei pra caralho o processo e a tatuagem', '@duda_kamaleoa', 'cliente'),
    ('Meudeus, ficou muito foda!!! Obrigada por topar e por me permitir ter a “releitura” dessa obra de arte! Seus traços são fodas!', 'mensagem de cliente', 'cliente'),
    ('Esse cara entende de tattoo', '@emanoel_taborda', ''),
    ('KRLLLL Q TATTOO INSANA MEU MANO', '@_rotten_moon_', 'cliente'),
]

WHATS = '5541997875360'
INSTA = 'https://www.instagram.com/harribtattoo_/'
