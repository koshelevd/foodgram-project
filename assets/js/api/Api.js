class Api {
  constructor(apiUrl) {
    this._apiUrl = apiUrl;
    this._headers = {
      'Content-Type': 'application/json',
      'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
    };
  }
  getPurchases() {
    return fetch(`${this._apiUrl}purchases/`, {
      headers: this._headers,
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addPurchases(id) {
    return fetch(`${this._apiUrl}purchases/`, {
      method: 'POST',
      headers: this._headers,
      body: JSON.stringify({
        recipe: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removePurchases(id) {
    return fetch(`${this._apiUrl}purchases/${id}/`, {
      method: 'DELETE',
      headers: this._headers,
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addSubscriptions(id) {
    return fetch(`${this._apiUrl}subscriptions/`, {
      method: 'POST',
      headers: this._headers,
      body: JSON.stringify({
        author: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions(id) {
    return fetch(`${this._apiUrl}subscriptions/${id}/`, {
      method: 'DELETE',
      headers: this._headers,
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addFavorites(id) {
    return fetch(`${this._apiUrl}favorites/`, {
      method: 'POST',
      headers: this._headers,
      body: JSON.stringify({
        recipe: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removeFavorites(id) {
    return fetch(`${this._apiUrl}favorites/${id}/`, {
      method: 'DELETE',
      headers: this._headers,
    })
      .then(e => {
        if (e.ok) {
          return e.json();
        }
        return Promise.reject(e.statusText)
      })
  }
  getIngredients(text) {
    return fetch(`${this._apiUrl}ingredients?query=${text}`, {
      headers: this._headers,
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
}
