from application import app


if __name__ == '__main__':
  app.secret_key = '<c\xbfX\x11\xed:H[\x8a<\x7f\x11\x02#S\xa0\xf9\x87\xfcs\xfc\x95\x0enG$\x93\xd8\x84\xd4/'
  app.debug = True
  app.run(host = '0.0.0.0', port=5000)