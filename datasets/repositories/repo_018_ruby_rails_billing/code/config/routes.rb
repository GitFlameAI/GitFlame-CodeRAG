Rails.application.routes.draw do
  resources :customers, only: [] do
    resources :subscriptions, only: [:create]
    resources :invoices, only: [:index]
  end

  resources :subscriptions, only: [] do
    member do
      post :cancel
    end
  end

  resources :invoices, only: [:show]

  resources :coupons, only: [:create] do
    collection do
      post :validate
    end
  end

  post "webhooks/payments", to: "webhooks#create"
end
