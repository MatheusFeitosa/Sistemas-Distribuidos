#O codigo tenta com o try achar o arquivo, se não achar ele retorna o erro, se achar ele quebra as linhas do arquivo e confere palavra por palavra

def achaPalavra(nome_arquivo, palavra):
	contador = 0
	
	try:
		arquivo = open(nome_arquivo, "r")



		for linha in arquivo:
    			palavras = linha.split()
    			for i in palavras:
    				if(i.lower() == palavra.lower()):
    					contador += 1	

		arquivo.close()
		
		return contador
	
	except:
		
		return "Documento nao encontrado"
	

programa = input()
palavra = input()

print(achaPalavra(programa, palavra))
