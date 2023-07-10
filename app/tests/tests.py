# from app import client
# from app.models import Post
# from datetime import datetime


# def test_get():
#     res = client.get('/api')

#     assert res.status_code == 200

#     assert len(res.get_json()) == len(Post.query.all())
#     assert res.get_json()[0]['id'] == 1


# def test_post():
#     data = {
#         'body': "post.body",
#         'timestamp': datetime(2022, 2, 18, 11, 2, 3, 000000),
#         'user_id': 1
#     }

#     res = client.post('/api', json=data)

#     assert res.status_code == 200


# def test_put():

#     res = client.put('/api/2', json={'body': "UPD"})

#     assert res.status_code == 200
#     assert Post.query.get(2).body == "UPD"


# def test_update():
#     res = client.delete('/api/2')

#     assert res.status_code == 204

#     assert Post.query.get(2) is None