import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs'

import { Configuration } from './configuration';

import { Document } from './models/document';
import { Article } from './models/article';

@Injectable()
export class VerseService {
	from = 'top';
	align = 'right';
	successMessage = 'Check Transaction Successful... ';
	failMessage = 'Sorry, you are unauthorized to perform the current transaction - please check with the app admin';


	private ApiLink: string;
	private APiPort: string;

	private GetAllDocuments: string;
	private GetArticlesByDoc: string;
	private CheckDocumentById: string;
    private DeleteDocument: string;
    private DeleteArticles: string;
	private DownloadCode: string;
    private SaveDocument: string;
    private SaveArticles: string;
    private SendNlp: string

	constructor(private HttpClient: HttpClient, private _configuration: Configuration) {
		this.GetAllDocuments = _configuration.GetAllDocuments;
		this.ApiLink = _configuration.ApiIP;
		this.APiPort = _configuration.ApiPort;
		this.GetArticlesByDoc = _configuration.GetArticlesByDoc;
		this.CheckDocumentById = _configuration.CheckDocumentById;
        this.DeleteDocument = _configuration.DeleteDocument;
        this.DeleteArticles = _configuration.DeleteArticles;
        this.DownloadCode = _configuration.DownloadCode;
        this.SaveDocument = _configuration.SaveDocument;
        this.SaveArticles = _configuration.SaveArticles;
        this.SendNlp = _configuration.SendNlp;
	}

	public getCodes(): Observable<Document[]> {
		return this.HttpClient.get<Document[]>(this.ApiLink + ':' + this.APiPort + '/', { withCredentials: false });
	}

	public getAllDocuments(): Observable<Document[]> {
		return this.HttpClient.get<Document[]>(this.ApiLink + ':' + this.APiPort + '/' + this.GetAllDocuments, { withCredentials: false });
	}

	public getDocument(doc_id: string): Observable<Document> {
		return this.HttpClient.get<Document>('/' + doc_id, { withCredentials: false });
	}

	public getArticle(art_id: string): Observable<Article> {
		return this.HttpClient.get<Article>('/' + art_id, { withCredentials: false });
	}

	public getArticlesByDocumentId(doc_id: string): Observable<Article[]> {
		return this.HttpClient.get<Article[]>(this.ApiLink + ':' + this.APiPort + '/' + this.GetArticlesByDoc + doc_id, { withCredentials: false });
	}

	public deleteDocument(doc_id: string) {
		return this.HttpClient.delete(this.ApiLink + ':' + this.APiPort + '/' + this.DeleteDocument + doc_id, { withCredentials: false });
    }

    public deleteArticles(doc_id: string) {
      return this.HttpClient.delete(this.ApiLink + ':' + this.APiPort + '/' + this.DeleteArticles + doc_id, { withCredentials: false });
    }

	public checkDocument(doc_id: string): Observable<Document> {
		console.log(this.ApiLink + ':' + this.APiPort + '/' + this.CheckDocumentById + doc_id + '/')
		return this.HttpClient.get<Document>(this.ApiLink + ':' + this.APiPort + '/' + this.CheckDocumentById + doc_id, { withCredentials: false });
	}

	public downloadCodeById(doc_id: string): Observable<Document> {
		return this.HttpClient.get<Document>(this.ApiLink + ':' + this.APiPort + '/' + this.DownloadCode + doc_id, { withCredentials: false });
	}

    public saveDocumentInBd(): Observable<string> {
        return this.HttpClient.post<string>(this.ApiLink + ':' + this.APiPort + '/' + this.SaveDocument, { withCredentials: false });
    }

    public nlpDocument(doc_id: string) {
      return this.HttpClient.put(this.ApiLink + ':' + this.APiPort + '/' + this.SendNlp + doc_id, { withCredentials: false });
    }

    public saveArticlesInBd(doc_id: string) {
      return this.HttpClient.post(this.ApiLink + ':' + this.APiPort + '/' + this.SaveArticles + doc_id, { withCredentials: false });
    }

}
