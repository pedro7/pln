from openpyxl import Workbook

from models import Comment


def create_xlsx(comments: list[Comment]):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Comentários"

    headers = (
        'Fórum',
        'Tópico',
        'Quantidade de respostas',
        'Quantidade de visualizações',
        'Criador do tópico',
        'Nome de usuário',
        'Conteúdo sujo',
        'Conteúdo limpo'

    )

    sheet.append(headers)

    for comment in comments:
        sheet.append((
            comment.forum.name,
            comment.topic.title,
            comment.topic.answers,
            comment.topic.views,
            comment.topic.username,
            comment.username,
            comment.raw_content,
            comment.clean_content
        ))

    workbook.save('comentarios.xlsx')
