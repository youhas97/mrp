<template>
    <div class="login-wrapper border border-light">
        <form class="form-signin" @submit.prevent="login">
            <h2 class="form-signin-heading">Please sign in</h2>
            <section>
            <label for="inputEmail" class="sr-only">Email address</label> <br/>
            <input v-model="email" type="email" id="inputEmail" class="form-control" placeholder="Email address" required autofocus>
            </section><section>
            <label for="inputPassword" class="sr-only">Password</label> <br/>
            <input v-model="password" type="password" id="inputPassword" class="form-control" placeholder="Password" required> <br/>
            <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
            </section>
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
    font-size: 24px;
}
section{
    padding: 10px;
}
label{
    font-size: 18px;
    color: #3CB371;
    padding: 7px;
}
button{
    margin: 12px;
}
</style>


