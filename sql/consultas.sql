-- Parte 4: exercícios com SQL
-- Execute no DB Browser for SQLite (aba "Executar SQL") ou na extensão SQLite do VS Code,
-- com o arquivo db.sqlite3 já populado por: python manage.py popular_banco
--
-- Tabelas criadas pelo Django para o app blog:
--   blog_post            (id, title, content, pub_date)
--   blog_comment         (id, text, pub_date, author_id, post_id)
--   blog_category        (id, name, description)
--   blog_post_categories (id, post_id, category_id)  -- tabela da relação muitos-para-muitos


-- 1) Todos os posts, ordenados pela data, sendo o mais recente primeiro
SELECT *
FROM blog_post
ORDER BY pub_date DESC;


-- 2) Para um post com comentários, todos os seus comentários
SELECT *
FROM blog_comment
WHERE post_id = (SELECT id FROM blog_post WHERE title = 'Amanhecer na Serra da Mantiqueira');


-- 3) Para um post com comentários, todos os seus comentários, com todas as colunas
--    da tabela de comentários (exceto post_id), o título do post e a data de
--    publicação do post renomeada para post_date
SELECT c.id,
       c.text,
       c.pub_date,
       c.author_id,
       p.title,
       p.pub_date AS post_date
FROM blog_comment AS c
JOIN blog_post AS p ON p.id = c.post_id
WHERE p.title = 'Amanhecer na Serra da Mantiqueira';


-- 4) Para uma categoria, todos os posts pertencentes a ela, com as colunas
--    da tabela de categoria e da tabela de posts
SELECT cat.*,
       p.*
FROM blog_category AS cat
JOIN blog_post_categories AS pc ON pc.category_id = cat.id
JOIN blog_post AS p ON p.id = pc.post_id
WHERE cat.name = 'Técnicas';


-- 5) Todas as categorias que possuem dois ou mais posts
SELECT cat.id,
       cat.name,
       COUNT(pc.post_id) AS total_posts
FROM blog_category AS cat
JOIN blog_post_categories AS pc ON pc.category_id = cat.id
GROUP BY cat.id, cat.name
HAVING COUNT(pc.post_id) >= 2;
