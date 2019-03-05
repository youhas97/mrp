<template>
    <div class="login-wrapper border border-light">
        <form class="form-signin" @submit.prevent="login">
            <h2 class="form-signin-heading">Please sign in</h2>
            <label for="inputEmail" class="sr-only">Email address</label>
            <input v-model="email" type="email" id="inputEmail" class="form-control" placeholder="Eamil address" required autofocus>
            <label for="inputPassword" class="sr-only">Password</label>
            <input v-model="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required>
            <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
        </form>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return{
            email: '',
            password:''
        }
    },
    methods: {
        login(){
            console.log(this.email)
            console.log(this.email)
        }
    }
}
</script>

<style scoped>
h2{
    color: #3CB371;
    font-weight: bold;
}
label{
    color: #3CB371;
    padding: 7px;
}
</style>


