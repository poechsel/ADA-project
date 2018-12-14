import twint

c = twint.Config()
c.Search = "#NotMyPresident"
c.Until = "2016-11-18"
c.Store_json=True
c.Output="nmp.json"

twint.run.Search(c)
