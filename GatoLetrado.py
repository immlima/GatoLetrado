import sqlite3
from sqlite3 import Error
#import time
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import requests
import bs4
from PIL import ImageTk, Image
from io import  BytesIO
import simplejson as json
import webbrowser


#|---Verificaçao da versao ---|
version="1.0"

def ver_versao():
    url="https://api.github.com/repos/immlima/GatoLetrado/releases/latest"
    v = requests.get(url)

    if v.status_code == requests.codes.OK:
        git_info=json.loads(v.text)
        if version!=str(git_info["tag_name"]):
            r=messagebox.askyesno("Versão disponível", "Nova versão está disponível para download.\n\nDeseja baixar a nova atualização?")
            if r==True:
                webbrowser.open('https://github.com/immlima/GatoLetrado', new=2)

window = Tk() 
window.deiconify()
#window.geometry("+500+400")
window.title("Biblioteca Virtual Gato Letrado")
window.iconphoto(TRUE, PhotoImage(file=os.path.join(os.path.abspath("."),"Data", "Assets","logo.png")))
window.resizable(FALSE,FALSE)


def conexaoBanco():
    caminho=os.path.join(os.path.abspath("."),"Data","data.db")
    con=None
    try:
       con=sqlite3.connect(caminho)  
    except Error as ex:
        print(ex)
    return con 
vcon=conexaoBanco()

def inserirbd(conexao,sql):
    try:
       c=conexao.cursor()
       c.execute(sql)  
       conexao.commit()
    except Error as ex:
        print(ex)
        return ex
    return c

def atualizarbd(conexao,sql):
    try:
       c=conexao.cursor()
       c.execute(sql)  
       conexao.commit()
    except Error as ex:
        print(ex)
    return c

def selectbd(conexao,sql):
    c=conexao.cursor()
    c.execute(sql)  
    return c.fetchall() 

tela_frame_main = LabelFrame(window, text="Biblioteca Virtual Gato Letrado : ")
tela_frame_main.grid(row=0, column=0, sticky=W, padx=5, pady=5)

tela_main = Frame(tela_frame_main)
tela_main.grid(row=0, column=0, sticky=W, padx=5, pady=5)
ORDER = "Nome"
ASN_ORDER=' ASC'
def search(event=None):
    global ORDER
    global ASN_ORDER

    if entry1tela1.get()=='':
        vsql="""SELECT Nome, autor, ISBN, genero, paginas, editora FROM livros WHERE 1"""
    else:
        vsql="""SELECT Nome, autor, ISBN, genero, paginas, editora FROM livros WHERE """
        vsql=vsql+str("""(Nome LIKE '%"""+entry1tela1.get().replace(" ","%' OR Nome LIKE '%")+"""%' OR autor LIKE '%"""+entry1tela1.get().replace(" ","%' OR autor LIKE '%")+"""%' OR ISBN LIKE '%"""+entry1tela1.get().replace(" ","%' OR ISBN LIKE '%")+"""%' OR genero LIKE '%"""+entry1tela1.get().replace(" ","%' OR genero LIKE '%")+"""%' OR paginas LIKE '%"""+entry1tela1.get().replace(" ","%' OR paginas LIKE '%")+"""%')""")
    vsql=vsql+str( """ ORDER BY """)+ORDER+ASN_ORDER
    #print(vsql)
    res=selectbd(vcon,vsql)
    for i in tv.get_children():
        tv.delete(i)
    global Count
    Count = 0
    for i in res:
        if Count % 2==0:
            tv.insert("","end",iid=Count, values=(i[0].replace("_"," "),i[1].replace("_"," "),i[2].replace("_"," "),i[3].replace("_"," "),i[4],i[5].replace("_"," ")), tags=('evenrow',))
        else:    
            tv.insert("","end",iid=Count, values=(i[0].replace("_"," "),i[1].replace("_"," "),i[2].replace("_"," "),i[3].replace("_"," "),i[4],i[5].replace("_"," ")), tags=('oddrow',))
        Count+= 1
    sub=len(res)
    vsql="""SELECT Nome, autor, ISBN, genero, paginas, editora FROM livros WHERE 1"""
    res=selectbd(vcon,vsql)
    total=len(res)
    if sub==total:
        text_total= "  "+"   "+"  "+"   "+str(total)
    else:
        text_total="   "+str(sub)+" / "+str(total)
    if total>1:
        text_total=text_total+" Livros"
    else:
        text_total=text_total+" Livro"
    Label( tela_main, text=text_total ).grid(row=12, column=0, padx=5, rowspan=11, columnspan=3, sticky=NE)

def deleteentry1tela1():
    entry1tela1.delete(0,99)
    search()

flabelframeFomat3 = LabelFrame(tela_main, text="Pesquisar : ", padx=5, pady=5)
entry1tela1=Entry(flabelframeFomat3, text="",bd=3, width=60)
entry1tela1.delete ( 0, last=99 )
entry1tela1.grid(row=0, column=1, sticky=NW, pady=2)
Button(flabelframeFomat3, text = " X ", command=deleteentry1tela1).grid(row=0, column=2, padx=5) 
Button(flabelframeFomat3, text = "🔎" , command=search).grid(row=0, column=3, padx=5) 
entry1tela1.bind('<Return>', search)
flabelframeFomat3.grid(row=0, column=0, sticky=NW, padx=5, pady=5)

style=ttk.Style()
style.theme_use('default')
style.configure("Treeview", background="#cca49b", foreground="black", fiedbackground="#D3D3D3",)
style.map('Treeview', background=[('selected','#C0705F')])

tree_scroll= Scrollbar(tela_main, orient="vertical")
tree_scroll.grid(row=1, column=4, pady=5, rowspan=11, columnspan=3, sticky=NS)
tv=ttk.Treeview(tela_main, columns=('Nome', 'autor', 'ISBN', 'genero', 'paginas', 'editora'), show='headings', height=15, yscrollcommand=tree_scroll.set, selectmode="extended")
tree_scroll.config(command=tv.yview)

def mud_oeder(c):
    global ORDER
    global ASN_ORDER
    ORDER = c
    if ASN_ORDER==' ASC':
       ASN_ORDER=' DESC' 
    else:
       ASN_ORDER=' ASC' 
    search()

tv.column('Nome', width=200)
tv.heading('Nome', text='Nome', command=lambda c='Nome': mud_oeder(c))

tv.column('autor', width=100)
tv.heading('autor', text='Autor', command=lambda c='autor': mud_oeder(c))

tv.column('ISBN', width=88, anchor=CENTER)
tv.heading('ISBN', text='ISBN-13', command=lambda c='ISBN': mud_oeder(c))

tv.column('genero', width=100)
tv.heading('genero', text='Gêneros', command=lambda c='genero': mud_oeder(c))

tv.column('paginas', width=60, anchor=CENTER)
tv.heading('paginas', text='Nº de Pag', command=lambda c='paginas': mud_oeder(c))

tv.column('editora', width=100)
tv.heading('editora', text='Editora', command=lambda c='editora': mud_oeder(c))

tv.tag_configure('oddrow', background="#cca49b")
tv.tag_configure('evenrow', background='white'  )
tv.grid(row=1, column=0, pady=5, rowspan=11, columnspan=3)
vsql=""" SELECT  Nome, autor, ISBN, genero, paginas, editora FROM livros ORDER BY Nome"""
#print(vsql)
res=selectbd(vcon,vsql)
global Count
Count = 0
for i in res:
    #print(i)
    #print(type(i))
    if Count % 2==0:
        tv.insert("","end",iid=Count, values=(i[0].replace("_"," "),i[1].replace("_"," "),i[2].replace("_"," "),i[3].replace("_"," "),i[4],i[5].replace("_"," ")), tags=('oddrow',))
    else:    
        tv.insert("","end",iid=Count, values=(i[0].replace("_"," "),i[1].replace("_"," "),i[2].replace("_"," "),i[3].replace("_"," "),i[4],i[5].replace("_"," ")), tags=('evenrow',))
    Count+= 1
def add_livro():

    def ISBN_j(event=None):
        try:
            res = requests.get("https://www.skoob.com.br/livro/lista/"+entryISBNtop.get())
            #res = requests.get("https://www.skoob.com.br/livro/lista/9788599170847")

            res.raise_for_status()
            ObjS=bs4.BeautifulSoup(res.text, 'html.parser')

            nome_livro = ObjS.select('.detalhes a')[0].get_text()
            #print(nome_livro)

            autores_livro = ObjS.select('.detalhes')[0].select('a[href*="tipo:autor/"]')
            ss=''
            for a in autores_livro:
                ss=ss+str(a.get_text())+", "
            autores_livro=ss[:-2]

            ano_livro = (ObjS.select('.detalhes  div  span')[0].get_text()).replace('Ano:','')
            print(ano_livro)
            #pag_livro = (ObjS.select('.detalhes')[0].select('span')[2].get_text()).replace(' / Páginas:','')
            pag_livro = (ObjS.select('.detalhes  div  span')[1].get_text()).replace(' / Páginas:','')
            

            editora = ObjS.select('.detalhes-2-sub')
            editora_t=str(editora[0]).replace('| ">',',">,')
            editora = bs4.BeautifulSoup(editora_t, 'html.parser').get_text()
            editora=editora.split("| ")[1]
            #print (editora)

            entryNometop.delete ( 0, last=99 )
            entryNometop.insert (0, nome_livro)
            entryAutortop.delete ( 0, last=99 )
            entryAutortop.insert (0, autores_livro)
            entryeEditoratop.delete ( 0, last=99 )
            entryeEditoratop.insert (0,editora)
            entryPaginastop.delete ( 0, last=99 )
            entryPaginastop.insert (0, pag_livro )
        except requests.exceptions.RequestException:
            pass

    def confirmar():
        if (entryNometop.get()=='') or  (entryAutortop.get()=='') or  (entryISBNtop.get()=='') :  
            messagebox.showinfo("Adicione um Livro", "Preencha todos os campos obrigatórios")
            top.deiconify()
        else:
            #print(entryPaginastop.get())
            if entryPaginastop.get().isnumeric() or entryPaginastop.get()=='':
                vsql='INSERT  INTO livros (Nome, autor, ISBN, genero, paginas, editora) VALUES ("'+entryNometop.get().lstrip(" ").rstrip(" ").replace(" ","_")+'"  , "'+entryAutortop.get().lstrip(" ").rstrip(" ").replace(" ","_")+'" , "'+entryISBNtop.get().lstrip(" ").rstrip(" ")+'"  , "'+entryGenerotop.get().lstrip(" ").rstrip(" ").replace(" ","_")+'"  , "'+entryPaginastop.get().lstrip(" ").rstrip(" ")+'"  , "'+entryeEditoratop.get().lstrip(" ").rstrip(" ").replace(" ","_")+ """")"""
                #print(vsql) or IGNORE 
                c = inserirbd(vcon,vsql)
                #print(vsql)
                if str(type(c)) =="<class 'sqlite3.IntegrityError'>":
                    messagebox.showinfo("Adicione um Livro", "Livro Duplicado, ISBN-13 já cadastrado")
                    top.deiconify()
                else:
                    deleteentry1tela1() 
                    top.destroy()
            else:
                messagebox.showinfo("Adicione um Livro", "Número de páginas inválida.")

    def cancel():
        deleteentry1tela1()
        top.destroy()

    top = Toplevel()
    top.resizable(FALSE,FALSE)
    top.geometry("+500+400")
    
    add_frame = LabelFrame(top, text="Adicione um Livro : ")
    add_frame.grid(row=0, column=0, columnspan=6, sticky=NW, padx=5, pady=2)
    
    Label( add_frame, text="ISBN-13* :" ).grid(row=0, column=0, sticky=NW)
    entryISBNtop=Entry(add_frame, text="",bd=3, width=51)
    entryISBNtop.delete ( 0, last=99 )
    entryISBNtop.grid(row=0, column=1, columnspan=3, sticky=NW, padx=5, pady=2)
    entryISBNtop.bind('<Return>', ISBN_j)

    Label( add_frame, text="Nome* :" ).grid(row=1, column=0, sticky=NW)
    entryNometop=Entry(add_frame, text="",bd=3, width=51)
    entryNometop.delete ( 0, last=99 )
    entryNometop.grid(row=1, column=1, columnspan=3, sticky=NW, padx=5, pady=2)

    Label( add_frame, text="Autor* :" ).grid(row=2, column=0, sticky=NW)
    entryAutortop=Entry(add_frame, text="",bd=3, width=51)
    entryAutortop.delete ( 0, last=99 )
    entryAutortop.grid(row=2, column=1, columnspan=3, sticky=NW, padx=5, pady=2)

    Label( add_frame, text="Gênero :" ).grid(row=3, column=0, sticky=NW)
    entryGenerotop=Entry(add_frame, text="",bd=3, width=51)
    entryGenerotop.delete ( 0, last=99 )
    entryGenerotop.grid(row=3, column=1, columnspan=3, sticky=NW, padx=5, pady=2)

    Label( add_frame, text="Páginas :" ).grid(row=4, column=0, sticky=NW)
    entryPaginastop=Entry(add_frame, text="",bd=3)
    entryPaginastop.delete ( 0, last=99 )
    entryPaginastop.grid(row=4, column=1, sticky=NW, padx=5, pady=2)

    Label( add_frame, text="Editora :" ).grid(row=4, column=2, sticky=NW)
    entryeEditoratop=Entry(add_frame, text="",bd=3)
    entryeEditoratop.delete ( 0, last=99 )
    entryeEditoratop.grid(row=4, column=3, sticky=NW, padx=5, pady=2)
    Label( add_frame, text="* Campos Obrigatórios" ).grid(row=5, column=3, sticky=NE, padx=5, pady=2)
    
    #ISBN_j()
    
    Button(top, text = "   Confirmar   ", command=confirmar).grid(row=1, column=2, padx=5, pady=3) 
    Button(top, text = "   Cancelar   ", command=cancel).grid(row=1, column=4, padx=5, pady=3) 

def propriedades(event=None):
    global tv
    if tv.item(tv.focus())['values']=='':
        messagebox.showinfo("Propriedades", "Selecione um Livro")
    else:
        def confirmar():
            if (entryNometop.get()=='') or  (entryAutortop.get()=='') or  (entryISBNtop.get()=='') :  
                messagebox.showinfo("Adicione um Livro", "Preencha todos os campos obrigatórios")
                top.deiconify()
            else:
                vsql="""UPDATE livros SET Nome='""" +entryNometop.get().replace(" ","_")+"""', autor='"""+entryAutortop.get().replace(" ","_")+"""', ISBN='"""+entryISBNtop.get()+"""', genero='"""+entryGenerotop.get().replace(" ","_")+"""', paginas='"""+entryPaginastop.get()+"""', editora='"""+entryeEditoratop.get().replace(" ","_")+"""' WHERE ID= '"""+str(res[0][6])+"""' """
                #print(vsql)
                atualizarbd(vcon,vsql)
                deleteentry1tela1()
                top.destroy()
                   
        def delete():
            top.deiconify()
            if messagebox.askyesno ("Excluir Livro", "Tem certeza de que deseja excluir este livro permanentemente?"):
                vsql="""SELECT ID FROM livros WHERE ISBN= '"""+str(tv.item(tv.focus())['values'][2])+"""'"""
                #print(vsql)
                res=selectbd(vcon,vsql) 
                #print(res[0][0])
                vsql="""DELETE FROM livros WHERE ID= '"""+str(res[0][0])+"""'"""
                atualizarbd(vcon,vsql)
                deleteentry1tela1()
                top.destroy()
            top.deiconify()

        def cancel():
            deleteentry1tela1()
            top.destroy()

        top = Toplevel()
        top.resizable(FALSE,FALSE)
        top.geometry("+500+400")
        #print(tv.item(tv.focus())['values'])
        vsql="""SELECT ID FROM livros WHERE ISBN= '"""+str(tv.item(tv.focus())['values'][2])+"""'"""
        #print(vsql)
        res=selectbd(vcon,vsql)
        #print(res)
        vsql="""SELECT Nome, autor, ISBN, genero, paginas, editora, ID FROM livros WHERE ID= '"""+str(res[0][0])+"""' """
        #print(vsql)
        res=selectbd(vcon,vsql)
        #print(res)

        add_frame = LabelFrame(top, text="Propriedades : ")
        add_frame.grid(row=0, column=0, columnspan=6, sticky=NW, padx=5, pady=2)

        Label( add_frame, text="ISBN-13* :" ).grid(row=0, column=0, sticky=NW)
        entryISBNtop=Entry(add_frame, text="",bd=3, width=51)
        entryISBNtop.delete ( 0, last=99 )
        entryISBNtop.grid(row=0, column=1, columnspan=3, sticky=NW, padx=5, pady=2)

        Label( add_frame, text="Nome* :" ).grid(row=1, column=0, sticky=NW)
        entryNometop=Entry(add_frame, text="",bd=3, width=51)
        entryNometop.delete ( 0, last=99 )
        entryNometop.grid(row=1, column=1, columnspan=3, sticky=NW, padx=5, pady=2)

        Label( add_frame, text="Autor* :" ).grid(row=2, column=0, sticky=NW)
        entryAutortop=Entry(add_frame, text="",bd=3, width=51)
        entryAutortop.delete ( 0, last=99 )
        entryAutortop.grid(row=2, column=1, columnspan=3, sticky=NW, padx=5, pady=2)

        Label( add_frame, text="Gênero :" ).grid(row=3, column=0, sticky=NW)
        entryGenerotop=Entry(add_frame, text="",bd=3, width=51)
        entryGenerotop.delete ( 0, last=99 )
        entryGenerotop.grid(row=3, column=1, columnspan=3, sticky=NW, padx=5, pady=2)

        Label( add_frame, text="Páginas :" ).grid(row=4, column=0, sticky=NW)
        entryPaginastop=Entry(add_frame, text="",bd=3)
        entryPaginastop.delete ( 0, last=99 )
        entryPaginastop.grid(row=4, column=1, sticky=NW, padx=5, pady=2)

        Label( add_frame, text="Editora :" ).grid(row=4, column=2, sticky=NW)
        entryeEditoratop=Entry(add_frame, text="",bd=3)
        entryeEditoratop.delete ( 0, last=99 )
        entryeEditoratop.grid(row=4, column=3, sticky=NW, padx=5, pady=2)
        Label( add_frame, text="* Campos Obrigatórios" ).grid(row=5, column=3, sticky=NE, padx=5, pady=2)
        
        entryNometop.delete ( 0, last=99 )
        entryNometop.insert (0, res[0][0].replace("_"," ") )

        entryAutortop.delete ( 0, last=99 )
        entryAutortop.insert (0, res[0][1].replace("_"," ") )
        
        entryISBNtop.delete ( 0, last=99 )
        entryISBNtop.insert (0, res[0][2] )

        entryGenerotop.delete ( 0, last=99 )
        entryGenerotop.insert (0, res[0][3].replace("_"," ") )

        entryPaginastop.delete ( 0, last=99 )
        entryPaginastop.insert (0, res[0][4] )

        entryeEditoratop.delete ( 0, last=99 )
        entryeEditoratop.insert (0,res[0][5].replace("_"," "))

        capa_frame = LabelFrame(top, text="Capa : ")
        capa_frame.grid(row=0, rowspan=10, column=99, sticky=NW, padx=5, pady=2)

        #print(url)
        try:
            url="http://covers.openlibrary.org/b/isbn/"+str(res[0][2])+"-M.jpg"
            jpg = requests.get(url)
            #print(jpg)
            img_data = jpg.content
            img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((123,185), Image.ANTIALIAS))
            panel = Label(capa_frame, image=img)
            panel.grid(row=0, column=0, sticky=NW, padx=5, pady=2)
        except requests.exceptions.RequestException:
            pass

        Button(top, text = "   Confirmar   ", command=confirmar).grid(row=1, column=1, columnspan=2, padx=5, pady=3) 
        Button(top, text = "   Deletar   ", command=delete, bg="#C0705F").grid(row=1, column=3, columnspan=2, padx=5, pady=3) 
        Button(top, text = "   Cancelar   ", command=cancel).grid(row=1, column=5, padx=5, pady=3) 

        top.mainloop()

tv.bind('<Double-Button-1>', propriedades)
Button(tela_main, text = "  ➕  ", command=add_livro).grid(row=0, column=1, padx=5, pady=10) 
Button(tela_main, text = "   📃   ", command=propriedades).grid(row=0, column=2, padx=5, pady=10) 

vsql="""SELECT Nome, autor, ISBN, genero, paginas, editora FROM livros WHERE 1"""
res=selectbd(vcon,vsql)
total=len(res)
if total>1:
    text_total="   "+"   "+str(total)+" Livros"
else:
    text_total="   "+"   "+str(total)+" Livro"

Label( tela_main, text=text_total ).grid(row=12, column=0, padx=5, rowspan=11, columnspan=3, sticky=NE)

def sobre():
    top = Toplevel()
    top.resizable(FALSE,FALSE)
    top.geometry("+500+400")   
    Label( top, text="v "+version ).grid(row=0, column=0, columnspan=3, padx=5, sticky=N)
    Label( top, text="Mateus Lima" ).grid(row=1, column=0, columnspan=3, padx=5, sticky=N)
    Label( top, text="mateuslpinho@gmail.com").grid(row=2, column=0, columnspan=3, padx=5, sticky=N)

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Novo livro", command=add_livro)
filemenu.add_command(label="Importar CSV")
filemenu.add_separator()
filemenu.add_command(label="Sair", command=window.quit)
menubar.add_cascade(label="Arquivo", menu=filemenu)

editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Propriedades", command=propriedades)
menubar.add_cascade(label="Editar", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Sobre...", command=sobre)
menubar.add_cascade(label="Ajuda", menu=helpmenu)

window.config(menu=menubar)
ver_versao()
window.mainloop()