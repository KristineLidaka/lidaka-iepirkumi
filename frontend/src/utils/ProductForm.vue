<template>
    <div>
        <h2 class="h3 mb-4">Pievienot jaunu produktu</h2>

        <div class="row g-3 align-items-end">
            <div class="col-md-4">
                <label for="article" class="form-label">Artikuls:</label>
                <input
                    id="article"
                    v-model="product.article"
                    type="text"
                    class="form-control"
                    :class="{ 'is-invalid': isEmptyField && !product.article }"
                />
            </div>

            <div class="col-md-3">
                <label for="quantity" class="form-label">Daudzums:</label>
                <input
                    id="quantity"
                    v-model="product.quantity"
                    type="number"
                    class="form-control"
                    min="0"
                    :class="{ 'is-invalid': isEmptyField && product.quantity === null }"
                />
            </div>

            <div class="col-md-3">
                <label for="price" class="form-label">Cena (EUR):</label>
                <input
                    id="price"
                    v-model="product.price"
                    type="number"
                    class="form-control"
                    step="0.01"
                    min="0"
                    :class="{ 'is-invalid': isEmptyField && product.price === null }"
                />
            </div>

            <div class="col-md-2">
                <button @click="addProduct" class="btn btn-primary w-100">Pievienot</button>
            </div>
        </div>
        <div v-if="products.length" class="product-list mt-4">
            <h3 class="h4 mb-3">Pievienotie produkti:</h3>
            <ul class="list-group mb-3">
                <li
                    v-for="item in products"
                    :key="item.uid"
                    class="list-group-item py-3"
                    :class="{
                        'list-group-item-danger': !!getErrorMessage(item.uid),
                    }"
                >
                    <div
                        class="d-flex flex-column flex-md-row justify-content-between align-items-md-center"
                    >
                        <div class="d-flex flex-wrap gap-3 gap-md-4 mb-2 mb-mb-0">
                            <div>
                                <small class="text-muted d-block">Artikuls</small>
                                <span class="fw-bold">{{ item.article }}</span>
                            </div>
                            <div>
                                <small class="text-muted d-block">Daudzums</small>
                                <span>{{ item.quantity }} gab.</span>
                            </div>
                            <div>
                                <small class="text-muted d-block">Cena</small>
                                <span>€{{ item.price }}</span>
                            </div>
                        </div>
                        <div v-if="getErrorMessage(item.uid)" class="text-danger fw-bold small">
                            <i class="bi bi-exclamation-triangle-fill me-1"></i>
                            {{ getErrorMessage(item.uid) }}
                        </div>
                    </div>
                </li>
            </ul>
            <div v-if="totalSumText" class="alert alert-success">
                <strong>Kopējā summa:</strong> {{ totalSumText }}
            </div>
            <button @click="handleCheck" class="btn btn-primary" :disabled="isLoading">
                Pārbaudīt
            </button>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { checkProduct } from '../services/productService';

const getEmptyProduct = () => ({ article: '', quantity: null, price: null });

const product = reactive(getEmptyProduct());
const products = ref([]);
const isLoading = ref(false);
const result = ref(null);
const validationErrors = ref([]);
const totalSumText = ref('');
const isEmptyField = ref(false);

const addProduct = () => {
    if (!product.article || product.quantity === null || product.price === null) {
        isEmptyField.value = true;
        return;
    }

    products.value.push({
        ...product,
        uid: crypto.randomUUID(),
    });

    Object.assign(product, getEmptyProduct());
    isEmptyField.value = false;
};

const handleCheck = async () => {
    isLoading.value = true;
    result.value = null;
    validationErrors.value = [];
    totalSumText.value = '';

    try {
        result.value = await checkProduct(products.value);
        if (result.value.status === 'error') {
            validationErrors.value = result.value.errors;
        } else {
            totalSumText.value = result.value.total_sum_text_lv;
        }
    } catch (error) {
        console.error(error);
        validationErrors.value = [{uid: 'system', error_msg: 'Kļūda savienojoties ar serveri'}];
    } finally {
        isLoading.value = false;
    }
};

const getErrorMessage = (uid) => {
    const error = validationErrors.value.find((err) => err.uid === uid);
    return error ? error.error_msg : '';
};
</script>
