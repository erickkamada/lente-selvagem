"""
Dados de exemplo usados pelo comando `python manage.py popular_banco`.

Atende ao mínimo pedido na parte 4 do enunciado:
- 4 posts: 1 sem comentários e 3 com várias categorias;
- os posts comentados têm de 2 a 3 comentários cada;
- 4 categorias, e todo post está em pelo menos uma.

As fotos ficam hospedadas no Wikimedia Commons (servidor externo).
"""
from datetime import datetime
from zoneinfo import ZoneInfo

FUSO = ZoneInfo('America/Sao_Paulo')


def quando(ano, mes, dia, hora, minuto):
    """Data e hora no fuso de São Paulo."""
    return datetime(ano, mes, dia, hora, minuto, tzinfo=FUSO)


def foto(arquivo, legenda, credito=None):
    """Bloco <figure> com a imagem servida pelo Wikimedia Commons."""
    pagina = f'https://commons.wikimedia.org/wiki/File:{arquivo}'
    imagem = f'https://commons.wikimedia.org/wiki/Special:FilePath/{arquivo}?width=1280'
    if credito:
        fonte = f'Foto: {credito}, via <a href="{pagina}">Wikimedia Commons</a>.'
    else:
        fonte = f'Foto: <a href="{pagina}">Wikimedia Commons</a> (autoria e licença na página do arquivo).'
    return (
        f'<figure>\n'
        f'  <img src="{imagem}" alt="{legenda}" loading="lazy">\n'
        f'  <figcaption>{legenda}. {fonte}</figcaption>\n'
        f'</figure>'
    )


CATEGORIAS = [
    ('Paisagens', 'Montanhas, vales, cachoeiras e a luz que muda tudo ao amanhecer e ao entardecer.'),
    ('Vida Selvagem', 'Aves, mamíferos e outros animais fotografados no seu ambiente, sem interferência.'),
    ('Macro', 'O mundo em escala de milímetros: gotas, insetos, flores e texturas.'),
    ('Técnicas', 'Configurações de câmera, equipamentos e truques de campo explicados passo a passo.'),
]

# (usuário, nome, sobrenome) — autores dos comentários
USUARIOS = [
    ('marina', 'Marina', 'Alves'),
    ('rafael', 'Rafael', 'Souza'),
    ('lucia', 'Lúcia', 'Prado'),
]

POSTS = [
    {
        'title': 'Amanhecer na Serra da Mantiqueira',
        'pub_date': quando(2026, 10, 5, 7, 40),
        'categories': ['Paisagens'],
        'content': '\n'.join([
            '<p>Saímos da pousada às 4h20, de lanterna na cabeça, para chegar ao mirante antes da hora azul. '
            'Na Mantiqueira, entre maio e setembro, o ar frio da madrugada costuma prender a neblina nos vales, '
            'e as cristas aparecem em camadas, cada uma num tom mais claro que a anterior.</p>',
            foto(
                'Serra_da_Mantiqueira_-_Acau%C3%A3_Cabral_(08).jpg',
                'Vista da Serra da Mantiqueira',
            ),
            '<p>A diferença de luz entre o céu e o vale é enorme nesse horário. Em vez de clarear tudo depois, '
            'uso um filtro degradê e faço a fotometria pelo céu, aceitando sombras mais escuras. '
            'O arquivo RAW segura bem a recuperação dessas áreas na edição.</p>',
            '<h3>Ponto de partida para cenas assim</h3>',
            '<ul>\n'
            '  <li>Tripé e disparo com temporizador de 2 s</li>\n'
            '  <li>ISO 100, abertura entre f/8 e f/11</li>\n'
            '  <li>Foco a um terço da cena</li>\n'
            '  <li>Chegar 40 minutos antes do nascer do sol</li>\n'
            '</ul>',
        ]),
        'comments': [
            ('marina', 'Que luz! Vale a pena acordar às 4h por um nascer do sol assim. Qual lente você usou?',
             quando(2026, 10, 5, 12, 10)),
            ('rafael', 'Dica anotada sobre o filtro degradê. Eu sempre estourava o céu nessas cenas.',
             quando(2026, 10, 6, 9, 25)),
            ('lucia', 'Estive no mesmo mirante em julho e a neblina não apareceu. Vou tentar de novo no inverno que vem.',
             quando(2026, 10, 7, 20, 2)),
        ],
    },
    {
        'title': 'Beija-flores no jardim: velocidade e paciência',
        'pub_date': quando(2026, 10, 14, 16, 20),
        'categories': ['Vida Selvagem', 'Técnicas'],
        'content': '\n'.join([
            '<p>Beija-flores batem as asas dezenas de vezes por segundo, então congelar o movimento exige '
            'velocidades de obturador muito altas ou flash. No jardim de casa, o beija-flor-tesoura '
            '(<em>Eupetomena macroura</em>) aparece todo fim de tarde, e foi assim que esta série começou.</p>',
            foto(
                'Beija-flor-tesoura_(Eupetomena_macroura)_-_Swallow-tailed_Hummingbird.jpg',
                'Beija-flor-tesoura (Eupetomena macroura)',
            ),
            '<p>O segredo foi observar antes de fotografar. Durante três dias anotei os horários e as flores '
            'preferidas. No quarto dia, montei a câmera no tripé a uns três metros, com o foco já ajustado na '
            'flor mais visitada, e esperei.</p>',
            '<p>Com luz natural, 1/2000 s congela o corpo, mas as asas ainda saem um pouco borradas, o que '
            'ajuda a contar a história do movimento. Para asas totalmente nítidas, só com flash em potência '
            'baixa, cuja duração curtíssima faz o papel do obturador.</p>',
            '<h3>Ponto de partida</h3>',
            '<ul>\n'
            '  <li>1/2000 s ou mais rápido, em prioridade de velocidade</li>\n'
            '  <li>Foco contínuo (AF-C) e disparo em sequência</li>\n'
            '  <li>Teleobjetiva entre 200 e 400 mm</li>\n'
            '  <li>Distância de 3 a 4 metros para não espantar a ave</li>\n'
            '</ul>',
        ]),
        'comments': [
            ('lucia', 'A 1/2000 s e as asas ainda borram? Impressionante a velocidade desses bichinhos.',
             quando(2026, 10, 14, 18, 45)),
            ('marina', 'Gostei da ideia de observar por alguns dias antes. Vou testar com os que visitam minha varanda.',
             quando(2026, 10, 15, 8, 30)),
        ],
    },
    {
        'title': 'Orvalho ao amanhecer: primeiros passos na fotografia macro',
        'pub_date': quando(2026, 10, 23, 6, 50),
        'categories': ['Macro', 'Técnicas'],
        'content': '\n'.join([
            '<p>O orvalho dura pouco: some assim que o sol começa a esquentar as folhas. Por isso, fotografar '
            'gotas em macro é um exercício de madrugada, de joelhos na grama molhada e sem pressa.</p>',
            foto('Dew_on_a_leaf.JPG', 'Gotas de orvalho sobre uma folha', 'Solar Police, CC BY-SA 4.0'),
            '<p>Na escala macro, a profundidade de campo tem poucos milímetros, mesmo em f/11, e qualquer brisa '
            'tira a gota do foco. Duas coisas ajudam: fotografar cedo, quando o vento costuma estar fraco, e usar '
            'foco manual, aproximando e afastando o corpo devagar até a gota ficar nítida.</p>',
            '<p>Não é preciso uma lente macro para começar. Tubos de extensão ou uma lente close-up de rosca, '
            'presos a uma objetiva comum, já permitem chegar bem perto. Cada gota funciona como uma pequena '
            'lente e inverte a paisagem atrás dela, então vale procurar um fundo colorido.</p>',
            '<h3>Ponto de partida</h3>',
            '<ul>\n'
            '  <li>Abertura entre f/8 e f/11 para ganhar alguns milímetros de nitidez</li>\n'
            '  <li>Foco manual com a tela ampliada (live view)</li>\n'
            '  <li>Rebatedor ou lanterna para clarear as sombras</li>\n'
            '  <li>Borrifador de água se o orvalho já tiver secado</li>\n'
            '</ul>',
        ]),
        'comments': [],  # o post sem comentários
    },
    {
        'title': 'Cachoeiras: como deixar a água com efeito de seda',
        'pub_date': quando(2026, 11, 2, 10, 5),
        'categories': ['Paisagens', 'Técnicas'],
        'content': '\n'.join([
            '<p>O efeito de água sedosa vem de exposições longas, de meio segundo a alguns segundos. Com o '
            'obturador aberto por mais tempo, cada gota deixa um rastro e a queda vira um véu contínuo, enquanto '
            'pedras e vegetação, imóveis, continuam nítidas.</p>',
            foto(
                'Cachoeira_do_Barroc%C3%A3o_09.jpg',
                'Cachoeira do Barrocão',
            ),
            '<p>Durante o dia, mesmo com ISO 100 e f/16, costuma haver luz demais para um segundo de exposição. '
            'É aí que entram os filtros ND (densidade neutra), que escurecem a cena sem mudar as cores: '
            'um ND de 6 pontos transforma 1/60 s em cerca de 1 s.</p>',
            '<p>Dias nublados ajudam muito, porque a luz fica uniforme e o branco da água não estoura. '
            'Um filtro polarizador também tira o reflexo das pedras molhadas e realça o verde da mata.</p>',
            '<h3>Ponto de partida</h3>',
            '<ul>\n'
            '  <li>Tripé firme e disparo remoto ou com temporizador</li>\n'
            '  <li>ISO 100, f/11 a f/16, de 0,5 s a 2 s</li>\n'
            '  <li>Filtro ND de 3 a 6 pontos em dias claros</li>\n'
            '  <li>Polarizador para cortar reflexos</li>\n'
            '</ul>',
        ]),
        'comments': [
            ('rafael', 'O cálculo do ND de 6 pontos ficou muito claro. Eu nunca sabia qual filtro comprar.',
             quando(2026, 11, 2, 14, 30)),
            ('lucia', 'Fui numa cachoeira no fim de semana e o polarizador fez toda a diferença nas pedras.',
             quando(2026, 11, 3, 21, 15)),
        ],
    },
]
